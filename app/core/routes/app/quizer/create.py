from fastapi import APIRouter, Depends, Path, Request, Cookie, HTTPException, UploadFile, File
from fastapi.responses import HTMLResponse
from ....database import get_db 
from ....models import UserToken, Tests, Questions, User, log_scoin_transaction
from typing import Annotated
from json import loads
from sqlalchemy import select, delete
from fastapi.templating import Jinja2Templates
from ....config import templates_path
from ....config import Settings
import io
import httpx
import json
import os
import uuid
from docx import Document
from datetime import datetime, timedelta, timezone

AI = Settings.AI
router = APIRouter(prefix="/create", tags=["create test"])
templates = Jinja2Templates(directory=templates_path)

GOOGLE_API_KEY = AI
UPLOAD_DIR = "static/uploads/quiz_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

AI_PROMPT = """
Sizga maktab fanlariga oid test savollari matni beriladi. Matn ichida tayyor HTML <img> teglari bo'lishi mumkin, ularga mutlaqo teginmang va ularni o'z joyida saqlang.
Ushbu matndan barcha savollarni ajratib oling va natijani JSON formatidagi massiv (array) ko'rinishida qaytaring. 

MUKAMMAL QOIDA:
1. Har bir element ichidagi "test-matn" va variantlar ("A", "B", "C", "D") qiymatlari  toza HTML formatida bo'lishi shart.
2. "correct" maydoniga doimo variantlar ichidan HAQIQATDAN HAM MATEMATIK VA MANTIQAN TO'G'RI BO'LGAN javob harfini ('A', 'B', 'C' yoki 'D') o'zingiz qayta hisoblab topib yozing! Shunchaki hamma savolga bir xil harf yozish QAT'IYAN TAQIQLANADI!

Struktura formati (Faqat format uchun namuna, javob harfi o'zgarishi shart):
[
  {
    "test-matn": "Savol matni shu yerda <b>muhim so'z</b>",
    "A": "A variant matni",
    "B": "B variant matni",
    "C": "C variant matni",
    "D": "D variant matni",
    "correct": "BU YERGA REAL TO'G'RI JAVOB HARFI YOZILSIN"
  }
]
"""
# =====================================================================
# 1. CREATE TEST PAGE (FAQAT 1 TA BO'LISHI SHART!)
# =====================================================================
@router.get("/", response_class=HTMLResponse)
async def create_test_page(request: Request, db = Depends(get_db), access_token: Annotated[str | None, Cookie()] = None):
    if not access_token:
        return HTMLResponse(content="<h1>Unauthorized</h1>", status_code=401)
    
    try:
        cookie = loads(access_token)
        query = select(UserToken).where(UserToken.token == cookie.get("token"))
        result = await db.execute(query)
        session = result.scalar_one_or_none()
        
        if not session or session.ip_address != request.client.host:
            return HTMLResponse(content="<h1>Unauthorized</h1>", status_code=401)
            
        user_query = await db.execute(select(User).where(User.id == session.user_id))
        user = user_query.scalar_one_or_none()
        if not user:
            return HTMLResponse(content="<h1>Unauthorized</h1>", status_code=401)
            
        response = templates.TemplateResponse(
            name="quizer/create.html",
            request=request, 
            context={
                "request": request, "username": user.username,
                "title": "Quizer - Test yaratish", "status": "AUTHORIZED",
                "background": user.background, "scoin": user.scoin
            }
        )
        return response
    except Exception as e:
        return HTMLResponse(content=f"<h1>Tizim xatoligi: {str(e)}</h1>", status_code=500)


# =====================================================================
# 2. CREATE TEST ENDPOINT (FAQAT 1 TA BO'LISHI SHART!)
# =====================================================================
@router.post("/create_test")
async def create_test(request: Request, db = Depends(get_db), access_token: Annotated[str | None, Cookie()] = None):
    if not access_token:
        raise HTTPException(status_code=401, detail="Xavfsizlik tokeni topilmadi")

    cookie = loads(access_token)
    query = select(UserToken).where(UserToken.token == cookie.get("token"))
    result = await db.execute(query)
    session = result.scalar_one_or_none()

    if not session or session.ip_address != request.client.host:
        raise HTTPException(status_code=401, detail="Sessiya yaroqsiz yoki IP mos kelmadi")

    user_query = await db.execute(select(User).where(User.id == session.user_id))
    user = user_query.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="Foydalanuvchi topilmadi")

    json_data = await request.json()
    name = json_data.get("name")
    description = json_data.get("description")

    if not name or not description:
        raise HTTPException(status_code=400, detail="Nom va tavsif kiritilishi shart")
        
    print(f"\n[LOG] >>> DASTUR FUNKSIYASI ISHLADI!")
    print(f"[LOG] >>> Test parametrlari: Name='{name}', Description='{description}'")
    
    try:
        # Obyekt yaratamiz
        new_test = Tests(title=name, description=description, user_id=user.id)
        
        # Asinxron sessiyaga qo'shish (Xavfsiz va to'g'ri standart)
        db.add(new_test)
         # Bazaga real yozish va ID olish
        await db.commit()          
        await db.refresh(new_test) 
        
        print(f"[LOG] >>> BAZAGA KO'CHIRILDI! Yangi Test ID: {new_test.id}")
        
        # Tekshiruv logi (Haqiqatni aniqlash uchun)
        check_query = await db.execute(select(Tests).where(Tests.user_id == user.id))
        all_tests = check_query.scalars().all()

        print("\n================ BAZADAGI REAL HOLAT ================")
        print(f"Jami topilgan testlar soni: {len(all_tests)}")
        for t in all_tests:
            print(f"ID: {t.id} | Title: {t.title} | Description: {t.description}")
        print("=====================================================\n")

        return {"message": "Test created successfully", "test_id": new_test.id}

    except Exception as e:
        await db.rollback()
        print(f"[LOG] >>> CRITICAL DATABASE ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Baza xatoligi: {str(e)}")


# =====================================================================
# 3. UPLOAD WORD AND AI GENERATE
# =====================================================================
@router.post("/upload-ai/{test_id}")
async def upload_word_and_generate_structured_html_ai(
    file: UploadFile = File(...), 
    db = Depends(get_db),
    test_id: int = Path(...)
):
    if not file.filename.endswith('.docx'):
        raise HTTPException(status_code=400, detail="Faqat Word (.docx) fayllarini yuklash mumkin!")
    
    print("\n[LOG] >>> Word fayl yuklash va AI jarayoni boshlandi...")
    try:
        file_bytes = await file.read()
        doc = Document(io.BytesIO(file_bytes))
        
        image_mapping = {}
        for rel_id, rel in doc.part.rels.items():
            if "image" in rel.target_ref:
                img_bytes = rel.target_part.blob
                ext = rel.target_ref.split('.')[-1]
                unique_img_name = f"{uuid.uuid4()}.{ext}"
                img_path = os.path.join(UPLOAD_DIR, unique_img_name)
                
                with open(img_path, "wb") as f:
                    f.write(img_bytes)
                
                image_mapping[rel_id] = f"/static/uploads/quiz_images/{unique_img_name}"

        full_text = []
        for paragraph in doc.paragraphs:
            p_text = paragraph.text.strip()
            if "r:embed" in paragraph._p.xml:
                for rel_id in image_mapping.keys():
                    if rel_id in paragraph._p.xml:
                        p_text += f' <br><img src="{image_mapping[rel_id]}" class="quiz-inline-img" alt="Test Rasm"><br>'
            if p_text:
                full_text.append(p_text)
                
        extracted_text = "\n".join(full_text)
        if not extracted_text.strip():
            raise HTTPException(status_code=400, detail="Word fayli bo'sh yoki ichida matn topilmadi!")
        # 🔥 SENING JADVALINGDA 500 TA LIMITI BOR BO'LGAN ENG ISHONCHLI MODEL URL manzili:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite:generateContent?key={GOOGLE_API_KEY}"
        
        headers = {"Content-Type": "application/json"}
        
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": f"{AI_PROMPT}\n\nMana test matni, barcha misollarni yechib, to'g'ri javobni 'correct' maydoniga yoz:\n{extracted_text}"
                }]
            }],
            "generationConfig": {
                "responseMimeType": "application/json"  # Toza JSON olish kafolati
            }
        }
        try:
            async with httpx.AsyncClient() as client:
                # timeout=None qilib qo'yamiz, so'rov uzilib ketmasligi uchun
                response = await client.post(url, headers=headers, json=payload, timeout=None)  

            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail=f"Google API xatoligi: {response.text}")

            res_json = response.json()
            ai_response_text = res_json['candidates'][0]['content']['parts'][0]['text'].strip()
            
            # Agar model javobni markdown ichida qaytarsa, tozalaymiz
            if ai_response_text.startswith("```json"):
                ai_response_text = ai_response_text.replace("```json", "").replace("```", "").strip()
            elif ai_response_text.startswith("```"):
                ai_response_text = ai_response_text.replace("```", "").strip()
                
            generated_questions = json.loads(ai_response_text)
            print(f"[LOG] >>> GEMINI 2.0 FLASH MUVAFFAQIYATLI HISOBLADI!")
            
        except Exception as ai_err:
            print(f"[LOG] >>> GEMINI 2.0 FLASH ERROR: {str(ai_err)}")
            raise HTTPException(status_code=500, detail=f"Google 2.0 AI javob bermadi: {str(ai_err)}")
        res_json = response.json()
        ai_response_text = res_json['candidates'][0]['content']['parts'][0]['text'].strip()
        generated_questions = json.loads(ai_response_text)

        inserted_count = 0
        for item in generated_questions:
            new_question = Questions(
                test_id=test_id,
                question_text=item.get("test-matn"),
                option_a=item.get("A"),
                option_b=item.get("B"),
                option_c=item.get("C"),
                option_d=item.get("D"),
                correct_answer=item.get("correct")
            )
            db.add(new_question)
            inserted_count += 1
            
        await db.commit()

        return {
            "status": "success",
            "message": f"AI  strukturani yaratdi! {inserted_count} ta savol bazaga yuklandi.",
            "data": generated_questions
        }

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Kutilmagan xatolik: {str(e)}")

@router.get("/cleanup-old-tests")
async def cleanup_old_empty_tests(db = Depends(get_db)):# 1. Hozirgi vaqtdan 1 soat oldingi vaqt nuqtasini hisoblaymiz
    bitta_soat_oldin = datetime.now(timezone.utc) - timedelta(hours=1)


    # 1 soatdan oldin yaratilgan va savollar ichida ID-si yo'q testlarni o'chiramiz
    query = delete(Tests).where(
        Tests.created_at < bitta_soat_oldin
    )

    # 3. So'rovni  ijro etamiz va bazani commit qilamiz
    await db.execute(query)
    await db.commit()

# =====================================================================
# 5. CONFIRM AND COMMIT TEST WITH DYNAMIC BILLING
# =====================================================================
@router.post("/confirm/{test_id}")
async def confirm_and_pay_test(
    request: Request,
    test_id: int = Path(...),
    is_private: bool = False,  # Frontenddan maxfiy yoki ommaviy test ekanligini olish uchun
    db = Depends(get_db),
    access_token: Annotated[str | None, Cookie()] = None
):
    if not access_token:
        raise HTTPException(status_code=401, detail="Xavfsizlik tokeni topilmadi")

    # 1. Foydalanuvchi va sessiyani tekshirish
    cookie = loads(access_token)
    query = select(UserToken).where(UserToken.token == cookie.get("token"))
    result = await db.execute(query)
    session = result.scalar_one_or_none()

    if not session or session.ip_address != request.client.host:
        raise HTTPException(status_code=401, detail="Sessiya yaroqsiz")

    user_query = await db.execute(select(User).where(User.id == session.user_id))
    user = user_query.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="Foydalanuvchi topilmadi")

    # 2. Testni va uning savollarini bazadan tekshirish
    test_query = await db.execute(select(Tests).where(Tests.id == test_id, Tests.user_id == user.id))
    test = test_query.scalar_one_or_none()
    if not test:
        raise HTTPException(status_code=404, detail="Test topilmadi")

    # Savollar sonini sanaymiz
    questions_query = await db.execute(select(Questions).where(Questions.test_id == test_id))
    questions_list = questions_query.scalars().all()
    questions_count = len(questions_list)

    # Frontenddan qo'shimcha argumentlarni olamiz (AI ishlatildimi yoki yo'q)
    body = await request.json()
    used_ai = body.get("used_ai", False)  # True yoki False keladi
    is_public = not body.get("is_private", True)  # Maxfiy test ekanligini olish

    # 🎯 DINAMIK NARXNI HISOBLASH TIZIMI
    BASE_TEST_PRICE = 4000     # 1. Yangi test yaratish
    AI_PRICE = 2000 if used_ai else 0  # 2. AI ishlatilgan bo'lsa
    SECRET_PRICE = 1000 if not is_public else 0  # 3. Maxfiy test bo'lsa (is_private=True)
    PER_QUESTION_PRICE = questions_count * 100  # 6. Har bir savol uchun 100 tadan

    # Jami  xarajat
    total_cost = BASE_TEST_PRICE + AI_PRICE + SECRET_PRICE + PER_QUESTION_PRICE

    print(f"\n[LOG] >>> DINAMIK BILLING HISOB-KITOBI:")
    print(f"[LOG] >>> Test ID: {test_id} | Savollar soni: {questions_count}")
    print(f"[LOG] >>> Base: {BASE_TEST_PRICE} | AI: {AI_PRICE} | Secret: {SECRET_PRICE} | Questions: {PER_QUESTION_PRICE}")
    print(f"[LOG] >>> JAMI NARX: {total_cost} sCoin | Foydalanuvchi balansi: {user.scoin} sCoin")

    # 3. Balans yetarli ekanligini tekshirish
    if user.scoin < total_cost:
        print(f"[LOG] >>> XATOLIK: sCoin mablag'i yetarli emas! {user.scoin} sCoin bor, {total_cost} sCoin kerak.")
        return {
            "status": "low_balance",
            "message": f"Hisobingizda mablag' yetarli emas. Jami: {total_cost} sCoin kerak. Sizda: {user.scoin} sCoin bor.",
            "required_scoin": total_cost,
            "current_scoin": user.scoin
        }

    try:
        # 4. Mablag'ni balansdan yechish
        user.scoin -= total_cost  # Testni maxfiy deb belgilaymiz
        await log_scoin_transaction(
            user_id=user.id,
            amount=-total_cost,
            description=f"Test yaratish: {test.title} ({questions_count} savol)",
            db=db,
        )
        # Testni to'liq tasdiqlangan holatga keltiramiz
        # Agar modelingizda status bo'lsa: test.status = "active" yoki test.is_active = True
        test.status = "active"  # Misol uchun, testni faol holatga o'tkazamiz
        test.is_public = is_public  # Maxfiy yoki ommaviy ekanligini saqlaymiz
        await db.commit()

        print(f"[LOG] >>> TO'LOV YA KUNLANDI! Yangi balans: {user.scoin} sCoin {is_public}")

        return {
            "status": "success",
            "message": f"Test muvaffaqiyatli tasdiqlandi va saqlandi! Balansdan {total_cost} sCoin yechildi.",
            "new_scoin": user.scoin,
            "total_cost": total_cost
        }

    except Exception as e:
        await db.rollback()
        print(f"[LOG] >>> YAKUNIY TO'LOVDA XATOLIK: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Billing tizimi xatoligi: {str(e)}")

@router.get("/reject-test/{test_id}")
async def reject_test(test_id: int = Path(...), db = Depends(get_db)):
    try:
        # Testni va unga tegishli savollarni o'chirish
        await db.execute(delete(Questions).where(Questions.test_id == test_id))
        await db.execute(delete(Tests).where(Tests.id == test_id))
        await db.commit()
        return {"status": "success", "message": f"Test ID {test_id} rad etildi va bazadan o'chirildi."}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Testni rad etishda xatolik: {str(e)}")