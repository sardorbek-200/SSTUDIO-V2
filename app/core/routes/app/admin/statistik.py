from fastapi import APIRouter, Depends, Cookie, Request, HTTPException 
from ....models import User, UserToken, Tests, TestResult, ScoinHistory
from fastapi.templating import Jinja2Templates
from typing import Annotated
from sqlalchemy import select, func
from ....config import templates_path
from fastapi.responses import HTMLResponse, RedirectResponse
from ....database import get_db
from .check import get_admin_user, checkadmin

template = Jinja2Templates(templates_path)
router = APIRouter()


@router.get("/static", response_class=HTMLResponse)
async def admin_dashboard(
    request: Request,
    db=Depends(get_db),
    access_token: Annotated[str, Cookie()] = None
):
    # 1. Admin foydalanuvchini tekshirish
    current_user = await get_admin_user(db, access_token)
    if not current_user:
        return RedirectResponse(url="/auth/sign-in", status_code=302)

    # 2. Huquqini tekshirish
    is_admin = await checkadmin(db, current_user)
    if not is_admin:
        raise HTTPException(status_code=403, detail="Siz admin emassiz")

    # 3. Yuqoridagi tezkor kartalar uchun ma'lumotlarni hisoblash
    # Jami ishlatilgan/aylangan sCoinlar yig'indisi (ScoinHistory'dagi barcha miqdorlar)
    scoin_sum_query = await db.execute(select(func.sum(ScoinHistory.amount)))
    total_scoin_used = scoin_sum_query.scalar() or 0

    # Tizimdagi jami faol sessiyalar (UserToken) soni
    active_sessions_query = await db.execute(select(func.count(UserToken.id)))
    active_sessions = active_sessions_query.scalar() or 0

    return template.TemplateResponse(
        name="admin/static.html",
        request=request,
        context={
            "request": request,
            "status": "AUTHORIZED",
            "title": "Kombinatsiyalangan Analitika",
            "username": current_user.username,
            "background": current_user.background,
            "total_scoin_used": total_scoin_used,
            "active_sessions": active_sessions
        }
    )


@router.get("/api/combined-chart-data")
async def get_combined_chart_data(db=Depends(get_db)):
    """
    Frontenddagi to'rttala chiziqli grafik uchun vaqt o'qi bo'yicha 
    tartiblangan barcha ma'lumotlarni yig'ib beruvchi universal API.
    """
    # 1. Foydalanuvchilar yaratilgan vaqti bo'yicha
    users_res = await db.execute(select(User).order_by(User.created_at.asc()))
    users = users_res.scalars().all()
    
    # 2. Yaratilgan testlar vaqti bo'yicha
    tests_res = await db.execute(select(Tests).order_by(Tests.created_at.asc()))
    tests = tests_res.scalars().all()
    
    # 3. Yakunlangan test natijalari vaqti bo'yicha
    results_res = await db.execute(select(TestResult).order_by(TestResult.created_at.asc()))
    results = results_res.scalars().all()
    
    # 4. sCoin operatsiyalari vaqti bo'yicha (Yangi qo'shilgan qism)
    scoin_res = await db.execute(select(ScoinHistory).order_by(ScoinHistory.created_at.asc()))
    scoin_hist = scoin_res.scalars().all()

    # Barcha ma'lumotlarni xom ko'rinishda (timestamp) frontendga JSON formatda qaytaramiz
    return {
        "users": [{"timestamp": u.created_at.timestamp()} for u in users],
        "tests": [{"timestamp": t.created_at.timestamp()} for t in tests],
        "results": [{"timestamp": r.created_at.timestamp()} for r in results],
        "scoin": [{"timestamp": s.created_at.timestamp()} for s in scoin_hist]
    }