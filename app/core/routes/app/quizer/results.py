from fastapi import APIRouter, Depends, HTTPException, Request, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from json import loads
from ....database import get_db
from ....models import TestResult, User, UserToken
from ....config import templates_path
router = APIRouter()

# Jinja2 sozlamasi (yo'lingizga qarab moslang)
templates = Jinja2Templates(directory=templates_path)

@router.get("/results/{test_id}", response_class=HTMLResponse)
async def view_test_results(request: Request, test_id: int, db: AsyncSession = Depends(get_db), access_token: Annotated[str | None, Cookie()] = None):
    """
    O'quvchilar natijalarini reyting tizimida (foiz bo'yicha balanddan pastga) ko'rsatish.
    Yuklab olish funksiyalari butunlay olib tashlandi.
    """
    # Avtorizatsiya tekshiruvi
    
    try:
        cookie = loads(access_token)
        token_str = cookie.get("token")
    except Exception:
        pass
    
    query = select(UserToken).where(UserToken.token == token_str)
    result = await db.execute(query)
    session = result.scalar_one_or_none()
    
    user_query = await db.execute(select(User).where(User.id == session.user_id))
    user = user_query.scalar_one_or_none()
    
    # test_results va unga tegishli user ma'lumotlarini birlashtirib, saralab olamiz
    query = (
        select(TestResult, User)
        .join(User, TestResult.user_id == User.id)
        .where(TestResult.test_id == test_id)
        .order_by(TestResult.percentage.desc(), TestResult.created_at.asc())
    )
    result = await db.execute(query)
    results_list = result.all()  # [(TestResult, User), ...] ko'rinishida qaytadi

    if not results_list:
        raise HTTPException(status_code=404, detail="Ushbu test bo'yicha hech qanday natija topilmadi!")

    return templates.TemplateResponse(
        name="/quizer/test_results.html",
        request=request,
        context={
            "request": request,
            "results": results_list,
            "test_id": test_id, 
            "background": user.background if user else "/static/images/default.png" ,
            "username": user.username,
            "status": "AUTHORIZED" if user else "UNAUTHORIZED",
            "title": "Natijalar"
        }
    )