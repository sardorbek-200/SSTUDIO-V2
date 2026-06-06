import bcrypt
from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from ...config import templates_path
from ...models import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ...database import get_db
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

auth = APIRouter()
templates = Jinja2Templates(directory=templates_path + "/auth")

@auth.get("/sign-up", response_class=HTMLResponse)
async def sign_up(request: Request, promo_code: str = None):
    return templates.TemplateResponse(
        request=request,
        name="sign-up.html",
        context={
            "request": request,
            "theme": "dark",
            "title": "Ro'yxatdan o'tish",
            "background": "/static/images/default_bg.png",
            "lang": "uz",
            "promo_code": promo_code
        }
    )

@auth.post("/sign-up", response_class=HTMLResponse)
async def sign_up_post(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    password_confirm: str = Form(...),
    promo_code_no: str = Form(""),
    db: AsyncSession = Depends(get_db),
):
    error = None
    if password != password_confirm:
        error = "Parollar mos emas."
    elif len(password) < 8:
        error = "Parol kamida 8 ta belgidan iborat bo'lishi kerak."
    if error:
        return templates.TemplateResponse(
            request=request,
            name="sign-up.html",
            context={
                "request": request,
                "theme": "dark",
                "title": "Ro'yxatdan o'tish",
                "background": "/static/images/default_bg.png",
                "lang": "uz",
                "error": error,
                "username": username,
                "promo_code_no": promo_code_no
            }
        )
    existing_user = await db.execute(select(User).where(User.username == username))
    if existing_user.scalar_one_or_none():
        error = "Bu foydalanuvchi nomi allaqachon band."
        return templates.TemplateResponse(
            request=request, name="sign-up.html",
            context={"request": request, "error": error, "username": username}
        )
    password_bytes = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode('utf-8')        # Parolni konsolga chiqarish (faqat test uchun, xavfsizlik uchun emas!)
    # 2. Yangi foydalanuvchini yaratamiz
    new_user = User(
        username=username,
        password=hashed_password, # Parolni xavfsiz hashlaymiz
        promo=promo_code_no                  # Promo kodni bazaga yozamiz
    )
    
    # 3. Bazaga qo'shamiz va saqlaymiz
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    # Muvaffaqiyatli ro'yxatdan o'tdi
    return RedirectResponse(url="/auth/sign-in", status_code=303)