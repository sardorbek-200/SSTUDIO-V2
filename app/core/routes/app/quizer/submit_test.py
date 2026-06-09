import json
import asyncio
import os
import base64
import httpx
from fastapi import APIRouter, Depends, HTTPException, status, Cookie
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramAPIError
from typing import Annotated

# Modellaringiz va konfiguratsiya joylashuvi
from ....database import get_db
from ....models import Tests, Questions, UserOptions, TestResult, AILearningAnalysis, TelegramAccount, UserToken, User
from .telegram import bot
from ....config import Settings

router = APIRouter(tags=["Finalize Test"])

GEMINI_API_KEY = Settings.AI
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite:generateContent?key={GEMINI_API_KEY}"

async def call_gemini_ai_for_test_analysis(questions_data: list) -> str:
    """
    Test savollarini mukammal o'quv-pedagogik tahlil qilish uchun 
    Gemini 3.1 REST API-siga toza HTTP so'rov yuborish.
    """
    system_instruction = (
        "Siz tajribali metodist va expert o'qituvchisiz. Sizga taqdim etilgan test savollarini "
        "tahlil qilib bering. Test qaysi mavzularni qamrab olgani, savollarning murakkablik darajasi, "
        "variantlarning to'g'ri tanlangani va testning umumiy sifati haqica batafsil "
        "pedagogik xulosa (tahlil) bering.Hamda Har bitta savolni qaysi javobda to'g'ri kelishini topib bering. Javobni chiroyli Markdown formatida va o'zbek tilida qaytaring."
    )

    parts = [{"text": "Tahlil qilinishi kerak bo'lgan test savollari ro'yxati:\n"}]

    for idx, q in enumerate(questions_data):
        question_text = (
            f"\nSavol raqami {idx+1}: {q['question']}\n"
            f"Variantlar: A) {q['options']['A']}, B) {q['options']['B']}, C) {q['options']['C']}, D) {q['options']['D']}\n"
            f"To'g'ri javob kaliti: {q['correct']}\n"
        )
        parts.append({"text": question_text})

        if q.get("image_path") and os.path.exists(q["image_path"]):
            try:
                with open(q["image_path"], "rb") as img_file:
                    img_base64 = base64.b64encode(img_file.read()).decode("utf-8")
                
                mime_type = "image/png" if q["image_path"].lower().endswith(".png") else "image/jpeg"
                parts.append({
                    "inlineData": {
                        "mimeType": mime_type,
                        "data": img_base64
                    }
                })
            except Exception as e:
                print(f"Rasmni o'qishda xatolik: {e}")

    payload = {
        "contents": [{"parts": parts}],
        "systemInstruction": {"parts": [{"text": system_instruction}]},
        "generationConfig": {
            "temperature": 0.2,
            "responseMimeType": "text/plain"
        }
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                GEMINI_URL, 
                json=payload, 
                headers={"Content-Type": "application/json"},
                timeout=50.0
            )
            if response.status_code == 200:
                res_json = response.json()
                return res_json['candidates'][0]['content']['parts'][0]['text']
            else:
                return f"AI Ekspertiza yuklanmadi (Status: {response.status_code}). Lekin test natijalari saqlandi!"
        except httpx.TimeoutException:
            return "Xatolik: AI tahlil qilish vaqti tugadi (Timeout). Lekin test natijalari muvaffaqiyatli saqlandi!"
        except Exception as e:
            return f"HTTP so'rovda kutilmagan xatolik: {str(e)}"


@router.post("/submit-test/{test_id}")
async def finalize_test(
    test_id: int, 
    db: AsyncSession = Depends(get_db),
    access_token: Annotated[str | None, Cookie()] = None
):
    if access_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Tizimga kirilmagan! Avtorizatsiya kaliti topilmadi."
        )
    
    try:
        session = json.loads(access_token)
        session_token = session.get("token")
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Yaroqsiz cookie formati."
        )

    user_token_query = await db.execute(select(UserToken).where(UserToken.token == session_token))
    user_token_obj = user_token_query.scalar_one_or_none()
    
    if not user_token_obj:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Sessiya eskirgan yoki haqiqiy emas."
        )
    
    user_query = await db.execute(select(User).where(User.id == user_token_obj.user_id))
    current_user = user_query.scalar_one_or_none()
    
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Foydalanuvchi topilmadi."
        )

    test_query = await db.execute(select(Tests).where(Tests.id == test_id))
    current_test = test_query.scalar_one_or_none()

    if not current_test:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="❌ Bunday test topilmadi!"
        )

    if current_test.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="🚫 Taqiqlangan! Siz faqat o'zingiz yaratgan testlarni yakunlay olasiz."
        )

    async def event_generator():
        try:
            yield "data: " + json.dumps({"status": "processing", "message": "⚙️ Test savollari va o'quvchilar javoblari tekshirilmoqda..."}) + "\n\n"
            await asyncio.sleep(0.3)

            q_query = select(Questions).where(Questions.test_id == test_id)
            q_result = await db.execute(q_query)
            questions = q_result.scalars().all()
            total_questions = len(questions)

            if total_questions == 0:
                yield "data: " + json.dumps({"status": "error", "message": "❌ Ushbu testda hech qanday savol topilmadi!"}) + "\n\n"
                return

            correct_keys = {str(q.id): q.correct_answer for q in questions}

            uo_query = select(UserOptions).where(UserOptions.test_id == test_id)
            uo_result = await db.execute(uo_query)
            user_options_list = uo_result.scalars().all()

            yield "data: " + json.dumps({"status": "processing", "message": "🤖 Sun'iy intellekt (AI) test mazmunini metodik tahlil qilmoqda..."}) + "\n\n"

            questions_archive_data = []
            for q in questions:
                questions_archive_data.append({
                    "id": q.id,
                    "question": q.question_text,
                    "options": {"A": q.option_a, "B": q.option_b, "C": q.option_c, "D": q.option_d},
                    "correct": q.correct_answer,
                    "image_path": q.image if hasattr(q, 'image') else None
                })

            questions_json_string = json.dumps(questions_archive_data, ensure_ascii=False)

            # Gemini API chaqirilmoqda (mana shu yerda 7-8 soniya kutadi)
            ai_analysis_content = await call_gemini_ai_for_test_analysis(questions_data=questions_archive_data)

            ai_analysis = AILearningAnalysis(
                test_id=test_id,
                analysis_text=ai_analysis_content,
                analysis_questions=questions_json_string
            )
            db.add(ai_analysis)
            await db.flush()    
            ai_id = ai_analysis.id

            yield "data: " + json.dumps({"status": "processing", "message": f"📊 {len(user_options_list)} ta o'quvchining natijalari hisoblanmoqda va Telegram xabarnomalar yuborilmoqda..."}) + "\n\n"

            for uo in user_options_list:
                try:
                    answers_list = json.loads(uo.options) if isinstance(uo.options, str) else uo.options
                except Exception:
                    answers_list = []
                
                correct_count = 0
                for ans_obj in answers_list:
                    q_id = str(ans_obj.get("q_id"))
                    user_ans = ans_obj.get("ans")
                    if correct_keys.get(q_id) == user_ans:
                        correct_count += 1

                percentage = (correct_count / total_questions) * 100 if total_questions > 0 else 0

                test_result = TestResult(
                    user_id=uo.user_id,
                    test_id=test_id,
                    correct_answers=correct_count,
                    total_questions=total_questions,
                    percentage=percentage
                )
                db.add(test_result)
                await db.flush()

                # Telegram ma'lumotlarini asinxron olish
                tg_query = select(TelegramAccount).where(TelegramAccount.user_id == uo.user_id)
                tg_result = await db.execute(tg_query)
                account = tg_result.scalars().first()

                if account and account.tg_id:
                    base_domain = "unsponsored-paulita-shakingly.ngrok-free.dev"
                    results_url = f"https://{base_domain}/app/quizer/results/{test_id}"
                    ai_url = f"https://{base_domain}/app/quizer/test/{ai_id}/analysis"
                    
                    wrong_count = total_questions - correct_count
                    
                    if percentage >= 90:
                        grade_status = "🥇 AJOYIB NATIJA! (A'lo)"
                    elif percentage >= 70:
                        grade_status = "🥈 JUDA ZO'R! (Yaxshi)"
                    elif percentage >= 50:
                        grade_status = "🥉 YOMON EMAS! (Qoniqarli)"
                    else:
                        grade_status = "📚 YANA BIR BOR O'QISH KERAK (Harakat qil!)"

                    # 🔥 TUZATISH: account.user.username o'rniga xavfsiz bo'lgan account.first_name ishlatildi!
                    # Bu greenlet_spawn xatosini butunlay yo'q qiladi.
                    display_name = account.first_name if account.first_name else "O'quvchi"

                    tg_message = (
                        f"🏁 <b>=== TEST YAKUNLANDI ===</b> 🏁\n\n"
                        f"👤 <b>O'quvchi:</b> {display_name}\n"
                        f"📋 <b>Umumiy savollar:</b> {total_questions} ta\n"
                        f"✅ <b>To'g'ri javoblar:</b> {correct_count} ta\n"
                        f"❌ <b>Xato javoblar:</b> {wrong_count} ta\n"
                        f"📈 <b>Ko'rsatkich:</b> <code>{percentage:.1f}%</code>\n"
                        f"🎯 <b>Natija:</b> <i>{grade_status}</i>\n\n"
                        f"-----------------------------------\n"
                        f"👇 <b>Kerakli foydali havolalar:</b>\n\n"
                        f"🥇 <a href='{results_url}'>📊 GURUH REYTINGINI KO'RISH</a>\n"
                        f"<i>(Kim nechanchi o'rinni olganini darhol bilib oling)</i>\n\n"
                        f"🧠 <a href='{ai_url}'>🤖 AI METODIK TAHLILINI O'QISH</a>\n"
                        f"<i>(Sun'iy intellekt sizga xatolaringizni tahlil qilib beradi)</i>\n\n"
                        f"✨ <i>Biz bilan o'sishda davom eting!</i>"
                    )
                    try:
                        await bot.send_message(
                            chat_id=account.tg_id,
                            text=tg_message,
                            parse_mode=ParseMode.HTML,
                            disable_web_page_preview=False
                        )
                    except (TelegramAPIError, Exception):
                        pass

            yield "data: " + json.dumps({"status": "processing", "message": "🧹 Bazani tozalash boshlandi: Savollar va vaqtinchalik javoblar o'chirilmoqda..."}) + "\n\n"
            
            # 🧹 Tozalash amallari ketma-ket asinxron bajariladi
            await db.execute(delete(Questions).where(Questions.test_id == test_id))
            await db.execute(delete(UserOptions).where(UserOptions.test_id == test_id))
            await db.execute(delete(Tests).where(Tests.id == test_id))

            # Yakuniy mukammal Commit!
            await db.commit()

            yield "data: " + json.dumps({"status": "success", "message": "🚀 Test muvaffaqiyatli yopildi, barcha ma'lumotlar arxivlandi va baza tozalandi!"}) + "\n\n"

        except Exception as e:
            await db.rollback()
            yield "data: " + json.dumps({"status": "error", "message": f"💥 Kutilmagan xatolik yuz berdi: {str(e)}"}) + "\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")