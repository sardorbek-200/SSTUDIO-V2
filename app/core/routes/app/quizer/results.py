from fastapi import APIRouter, Depends, HTTPException, Request, Cookie
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
import json
from ....database import get_db
from ....models import TestResult, User, UserToken
from ....config import templates_path

router = APIRouter()

# Jinja2 sozlamasi
templates = Jinja2Templates(directory=templates_path)

@router.get("/results/{test_id}", response_class=HTMLResponse)
async def view_test_results(
    request: Request, 
    test_id: int, 
    db: AsyncSession = Depends(get_db), 
    access_token: Annotated[str | None, Cookie()] = None
):
    """
    O'quvchilar natijalarini reyting tizimida ko'rsatish.
    🔥 Tizimga kirmagan MEHMONLAR uchun ham kirishga ruxsat berildi!
    """
    # 🏁 1-QADAM: Standart qiymatlar (Mehmon holati uchun)
    username = "Mehmon"
    background_img = "/static/images/default_bg.png"
    status = "UNAUTHORIZED"
    user = None 

    # 🔐 2-QADAM: Avtorizatsiya tekshiruvi (Faqat cookie bor bo'lsa tekshiradi)
    if access_token:
        try:
            cookie = json.loads(access_token)
            token_str = cookie.get("token")
            
            query = select(UserToken).where(UserToken.token == token_str)
            result = await db.execute(query)
            session = result.scalar_one_or_none()
            
            if session:
                user_query = await db.execute(select(User).where(User.id == session.user_id))
                user = user_query.scalar_one_or_none()
                
                if user:
                    username = user.username
                    status = "AUTHORIZED"
                    if user.background:
                        background_img = user.background
        except Exception:
            pass  # Cookie buzilgan bo'lsa ham xato bermaydi, mehmon bo'lib davom etadi

    # 🛑 DIQQAT: Boyagi RedirectResponse olib tashlandi! 
    # Endi user None bo'lsa ham kod pastga qarab daxshatli silliq o'tib ketaveradi.

    # 📊 3-QADAM: Test natijalarini bazadan reyting bo'yicha saralab olamiz
    query = (
        select(TestResult, User)
        .join(User, TestResult.user_id == User.id)
        .where(TestResult.test_id == test_id)
        .order_by(TestResult.percentage.desc(), TestResult.created_at.asc())
    )
    result = await db.execute(query)
    results_list = result.all()  # [(TestResult, User), ...]

    if not results_list:
        raise HTTPException(status_code=404, detail="Ushbu test bo'yicha hech qanday natija topilmadi!")

    # 🟢 4-QADAM: Jinja2 shabloniga context yuboramiz
    return templates.TemplateResponse(
        name="quizer/test_results.html",
        request=request,
        context={
            "request": request,
            "results": results_list,
            "test_id": test_id, 
            "background": background_img,
            "username": username,
            "status": status,
            "title": "Natijalar"
        }
    )