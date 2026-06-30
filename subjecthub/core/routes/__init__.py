from json import loads, dumps
from typing import Annotated
from fastapi import APIRouter, Request, Depends, Cookie
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession


# Nisbiy yo'llar orqali faqat bor narsalarni import qilamiz
from ..models import User, UserToken
from ...config import templates_path
from ..database import get_db,init_db

from .admin import router as adminrouter
from .adminapi import router as adminapirouter
from .play import router as playrouter

# Jinja2 andozalar drayveri
templates = Jinja2Templates(directory=templates_path)


# Markaziy router (Hozircha faqat shu fayldagi yo'llar ishlaydi)
router = APIRouter(prefix="/subjecthub")

router.include_router(adminapirouter)
router.include_router(adminrouter)
router.include_router(playrouter)


@router.get("/", response_class=HTMLResponse)
async def home_page(
    request: Request,
    db: AsyncSession = Depends(get_db),
    access_token: Annotated[str | None, Cookie()] = None
):
    # Umumiy foydalanuvchilar soni va top-3 kiber-shavvozlar reytingi
    total_users_query = await db.execute(select(func.count(User.id)))
    total_users = total_users_query.scalar()
    
    top_users_query = await db.execute(
        select(User).order_by(User.xp.desc()).limit(15)
    )
    top_users = top_users_query.scalars().all()
        
    # 1. Agar cookie yo'q bo'lsa, UNAUTHORIZED statusda andozani yuboramiz
    if not access_token:
        return templates.TemplateResponse(name="index.html", request=request, context={
            "request": request,
            "status": "UNAUTHORIZED",
            "theme": "dark",
            "total_users": total_users,
            "top_users": top_users,
            "title": "Bosh sahifa",
            "background": "/static/images/default_bg.png",
            "lang": "uz" 
        })
        
    try:
        # Cookie ichidan tokenni ajratib olamiz
        cookie = loads(access_token)
        query = select(UserToken).where(UserToken.token == cookie.get("token"))
        result = await db.execute(query)
        session = result.scalar_one_or_none()
    except Exception:
        session = None
    
    # 2. Agar sessiya topilmasa yoki IP manzil mos kelmasa, andoza UNAUTHORIZED bo'lib ketadi
    if not session or session.ip_address != request.client.host:
        return templates.TemplateResponse(name="index.html", request=request, context={
            "request": request,
            "status": "UNAUTHORIZED",
            "theme": "dark",
            "total_users": total_users,
            "top_users": top_users,
            "title": "Bosh sahifa",
            "background": "/static/images/default_bg.png",
            "lang": "uz" 
        })
        
    # Foydalanuvchini tekshiramiz
    user_query = await db.execute(select(User).where(User.id == session.user_id))
    user = user_query.scalar_one_or_none()
    
    if not user:
        raise Exception("User not found")
        
    # 3. Agar hamma narsa to'g'ri bo'lsa, AUTHORIZED holatda foydalanuvchi ma'lumotlari bilan yuboramiz
    response = templates.TemplateResponse(name="index.html", request=request, context={
        "request": request,
        "status": "AUTHORIZED",
        "theme": "dark",
        "username": user.username,
        "total_users": total_users,
        "top_users": top_users,
        "background": user.background,
        "title": "Bosh sahifa",
        "scoin":user.scoin,
        "xp":user.xp
    })
    
    return response