from fastapi import APIRouter, Depends, Form, Request # Request ni import qilishni unutmang!
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import json
from ...database import get_db
from app.core.database import get_db
import uuid
from ...models import UserToken
from json import dumps
from app.core.database import get_db
from ...config import templates_path
import bcrypt
from ...models import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
auth = APIRouter()
templates = Jinja2Templates(directory=templates_path+"/auth") # auth uchun alohida papka yaratdik
@auth.get("/sign-in", response_class=HTMLResponse)
async def sign_in(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="sign-in.html", 
        context={
            "request": request,
            "theme": "dark",
            "title": "Kirish sahifasi",
            "background": "/static/images/default_bg.png",
            "lang": "uz"
        }
    )
@auth.post("/sign-in", response_class=HTMLResponse)
async def sign_in_post(
    request: Request,
    username: str = Form(...), 
    password: str = Form(...),
    db: AsyncSession = Depends(get_db), # Tayyor ulangan sessiya
):
    if len(password) < 8:
        error = "Parol kamida 8 ta belgidan iborat bo'lishi kerak."
        return templates.TemplateResponse(
            request=request, 
            name="sign-in.html", 
            context={
                "request": request, "theme": "dark", "title": "Kirish sahifasi",
                "background": "/static/images/default_bg.png", "lang": "uz",
                "error": error, "username": username
            }
        )

    # --- TO'G'RILANGAN JOYI: async with satrini o'chirib, to'g'ridan-to'g'ri db'dan foydalanamiz ---
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    
    if not user:
        error = "Foydalanuvchi topilmadi."
        return templates.TemplateResponse(
            request=request, 
            name="sign-in.html", 
            context={
                "request": request, "theme": "dark", "title": "Kirish sahifasi",
                "background": "/static/images/default_bg.png", "lang": "uz",
                "error": error, "username": username
            }
        )
        
    if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        error = "Parol noto'g'ri."
        return templates.TemplateResponse(
            request=request, 
            name="sign-in.html", 
            context={
                "request": request, "theme": "dark", "title": "Kirish sahifasi",
                "background": "/static/images/default_bg.png", "lang": "uz",
                "error": error, "username": username
            }
        )
    random_token = str(uuid.uuid4())
    client_ip = request.client.host
    user_token = UserToken(
        token=random_token,
        user_id=user.id,
        ip_address=client_ip
    )
    db.add(user_token)
    await db.commit()
    
    # Agar hammasi muvaffaqiyatli bo'lsa, foydalanuvchini bosh sahifaga yo'naltiramiz
    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(key="access_token", value=dumps({'token':random_token}), httponly=True) # 10 daqiqa
    return response