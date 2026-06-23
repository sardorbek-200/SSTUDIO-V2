from json import loads
from fastapi import APIRouter, Request, Depends, Cookie, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated
from sqlalchemy.future import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.models import UserToken, User, Tests, Questions
from ..admin.check import checkadmin
from ....config import templates_path

templates = Jinja2Templates(directory=templates_path)
router = APIRouter(tags=["Quizer Dynamic Edit"])

# Foydalanuvchini cookie orqali aniqlash helper funksiyasi
async def get_current_user(db: AsyncSession, access_token: str):
    if not access_token:
        return None
    try:
        cookie = loads(access_token)
        token_str = cookie.get("token")
    except Exception:
        return None
    
    query = select(UserToken).where(UserToken.token == token_str)
    result = await db.execute(query)
    return result.scalar_one_or_none()

# --------------------------------------------------------------------------
# 🌐 1. ASOSIY TAHRIRLASH SAHIFASI (TESTLAR RO'YXATI BILAN)
# --------------------------------------------------------------------------
@router.get("/edit", response_class=HTMLResponse)
async def edit_main_page(
    request: Request, 
    db: AsyncSession = Depends(get_db), 
    access_token: Annotated[str | None, Cookie()] = None
):
    session = await get_current_user(db, access_token)
    if not session or session.ip_address != request.client.host:
        return RedirectResponse(url="/auth/login")
        
    user_query = await db.execute(select(User).where(User.id == session.user_id))
    user = user_query.scalar_one_or_none()
    if not user:
        return RedirectResponse(url="/auth/login")

    # Barcha mavjud testlarni select qilish (o'quvchi/admin tanlashi uchun)
    tests_query = await db.execute(select(Tests).where(Tests.status=='active',Tests.user_id==user.id))
    all_tests = tests_query.scalars().all()

    return templates.TemplateResponse(
        name="quizer/edit_test.html", 
        request=request, 
        context={
            "request": request,
            "username": user.username,
            "title": "Testlarni Tahrirlash",
            "scoin": user.scoin,
            "status":"AUTHORIZED",
            "background": user.background,
            "tests": all_tests  # Frontend select qismiga boradi
        }
    )

# --------------------------------------------------------------------------
# ⚡ 2. API ENDPOINT: TANLANGAN TEST MA'LUMOTLARINI DINAMIK OLISH
# --------------------------------------------------------------------------
@router.get("/api/get-test/{test_id}")
async def api_get_test_data(
    test_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db),
    access_token: Annotated[str | None, Cookie()] = None,
):
    # Faqat test muallifi yoki admin test ma'lumotlarini olishi mumkin
    session = await get_current_user(db, access_token)
    if not session or session.ip_address != request.client.host:
        return JSONResponse({"status": "error", "message": "Unauthorized"}, status_code=401)

    user_q = await db.execute(select(User).where(User.id == session.user_id))
    user = user_q.scalar_one_or_none()
    if not user:
        return JSONResponse({"status": "error", "message": "Unauthorized"}, status_code=401)

    # Test mantiqini olish
    test_query = await db.execute(select(Tests).where(Tests.id == test_id))
    test = test_query.scalar_one_or_none()
    if not test:
        return JSONResponse({"status": "error", "message": "Test topilmadi"}, status_code=404)

    # Egasi yoki admin bo'lmasa ruxsat yo'q
    if test.user_id != user.id:
        is_admin = await checkadmin(db, user)
        if not is_admin:
            return JSONResponse({"status": "error", "message": "Access denied"}, status_code=403)

    # Savollarni olish
    questions_query = await db.execute(select(Questions).where(Questions.test_id == test_id))
    questions = questions_query.scalars().all()

    # JSON formatga o'giramiz
    questions_data = []
    for q in questions:
        questions_data.append({
            "id": q.id,
            "question_text": q.question_text,
            "option_a": q.option_a,
            "option_b": q.option_b,
            "option_c": q.option_c,
            "option_d": q.option_d,
            "correct_option": q.correct_answer
        })

    return {
        "status": "success",
        "test": {
            "id": test.id,
            "title": test.title,
            "description": test.description,
            "status": test.status
        },
        "questions": questions_data
    }
# --------------------------------------------------------------------------
# 🔄 SAVOL VA VARIANTLARNI YANGILASH (POST/PUT API)
# --------------------------------------------------------------------------
@router.post("/edit/question/{question_id}/update")
async def update_question_data(
    question_id: int,
    data: dict,
    db: AsyncSession = Depends(get_db),
    access_token: Annotated[str | None, Cookie()] = None,
):
    try:
        # Avvalo so'rov yuborgan foydalanuvchini aniqlaymiz
        session = await get_current_user(db, access_token)
        if not session:
            return JSONResponse({"status": "error", "message": "Unauthorized"}, status_code=401)

        user_q = await db.execute(select(User).where(User.id == session.user_id))
        user = user_q.scalar_one_or_none()
        if not user:
            return JSONResponse({"status": "error", "message": "Unauthorized"}, status_code=401)

        # So'rov qilingan savol va uning testi mavjudligini tekshiramiz
        q_query = await db.execute(select(Questions).where(Questions.id == question_id))
        q_obj = q_query.scalar_one_or_none()
        if not q_obj:
            return JSONResponse({"status": "error", "message": "Savol topilmadi"}, status_code=404)

        test_query = await db.execute(select(Tests).where(Tests.id == q_obj.test_id))
        test = test_query.scalar_one_or_none()
        if not test:
            return JSONResponse({"status": "error", "message": "Test topilmadi"}, status_code=404)

        # Faqat test muallifi yoki admin tahrirlashi mumkin
        if test.user_id != user.id:
            is_admin = await checkadmin(db, user)
            if not is_admin:
                return JSONResponse({"status": "error", "message": "Access denied"}, status_code=403)

        # Kelayotgan ma'lumotlarni model maydonlariga moslab olamiz
        stmt = update(Questions).where(Questions.id == question_id).values(
            question_text=data.get("question_text"),
            option_a=data.get("option_a"),
            option_b=data.get("option_b"),
            option_c=data.get("option_c"),
            option_d=data.get("option_d"),
            correct_answer=data.get("correct_option")
        )
        await db.execute(stmt)
        await db.commit()
        return {"status": "success", "message": f"Savol #{question_id} muvaffaqiyatli yangilandi!"}
    except Exception as e:
        await db.rollback()
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)

# --------------------------------------------------------------------------
# ⚙️ TEST ASOSIY INFOSINI YANGILASH (POST API)
# --------------------------------------------------------------------------
@router.post("/edit/{test_id}/update-info")
async def update_test_info(
    test_id: int,
    data: dict,
    db: AsyncSession = Depends(get_db),
    access_token: Annotated[str | None, Cookie()] = None,
):
    try:
        # Avvalo so'rov yuborgan foydalanuvchini aniqlaymiz
        session = await get_current_user(db, access_token)
        if not session:
            return JSONResponse({"status": "error", "message": "Unauthorized"}, status_code=401)

        user_q = await db.execute(select(User).where(User.id == session.user_id))
        user = user_q.scalar_one_or_none()
        if not user:
            return JSONResponse({"status": "error", "message": "Unauthorized"}, status_code=401)

        # Testni olamiz va muallifligini tekshiramiz
        test_query = await db.execute(select(Tests).where(Tests.id == test_id))
        test = test_query.scalar_one_or_none()
        if not test:
            return JSONResponse({"status": "error", "message": "Test topilmadi"}, status_code=404)

        if test.user_id != user.id:
            is_admin = await checkadmin(db, user)
            if not is_admin:
                return JSONResponse({"status": "error", "message": "Access denied"}, status_code=403)

        # Kelgan JSON ma'lumotlarini bazada yangilaymiz
        stmt = update(Tests).where(Tests.id == test_id).values(
            title=data.get("title"),
            description=data.get("description"),
            status=data.get("status")
        )
        await db.execute(stmt)
        await db.commit()
        return {"status": "success", "message": "Testning umumiy sozlamalari muvaffaqiyatli saqlandi!"}
    except Exception as e:
        await db.rollback()
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)