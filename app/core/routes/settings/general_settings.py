from fastapi import APIRouter, Depends, Form, Request, Cookie
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from json import loads, dumps
from typing import Annotated
from ...database import get_db
from ...models import User, UserToken

router = APIRouter()


def get_current_user(
    db: AsyncSession = Depends(get_db),
    access_token: Annotated[str | None, Cookie()] = None
):
    """Joriy foydalanuvchini cookiedan o'qib olish"""
    if not access_token:
        return None
    try:
        cookie = loads(access_token)
        token = cookie.get("token")
        return token
    except:
        return None


@router.get("/general")
async def get_general_settings(
    db: AsyncSession = Depends(get_db),
    access_token: Annotated[str | None, Cookie()] = None
):
    """Foydalanuvchi umumiy sozlamalarini olish"""
    if not access_token:
        return JSONResponse(
            status_code=401,
            content={"error": "Avtentifikatsiya talab qilinadi"}
        )
    
    try:
        cookie = loads(access_token)
        token = cookie.get("token")
        
        # Token orqali userga kirish
        query = select(UserToken).where(UserToken.token == token)
        result = await db.execute(query)
        session = result.scalar_one_or_none()
        
        if not session:
            return JSONResponse(
                status_code=401,
                content={"error": "Token noto'g'ri yoki eskirgan"}
            )
        
        # Userga kirish
        user_query = await db.execute(select(User).where(User.id == session.user_id))
        user = user_query.scalar_one_or_none()
        
        if not user:
            return JSONResponse(
                status_code=404,
                content={"error": "Foydalanuvchi topilmadi"}
            )
        
        return JSONResponse(
            status_code=200,
            content={
                "username": user.username,
                "language": user.language,
                "theme": "dark",
                "background": user.background,
                "scoin": user.scoin,
                "xp": user.xp,
                "created_at": str(user.created_at)
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Xatolik: {str(e)}"}
        )


@router.get("/api/user/stats")
async def get_user_stats(
    db: AsyncSession = Depends(get_db),
    access_token: Annotated[str | None, Cookie()] = None
):
    """Foydalanuvchi statistikasini JSON formatida qaytarish"""
    if not access_token:
        return JSONResponse(
            status_code=401,
            content={"error": "Avtentifikatsiya talab qilinadi"}
        )

    try:
        cookie = loads(access_token)
        token = cookie.get("token")

        query = select(UserToken).where(UserToken.token == token)
        result = await db.execute(query)
        session = result.scalar_one_or_none()

        if not session:
            return JSONResponse(
                status_code=401,
                content={"error": "Token noto'g'ri yoki eskirgan"}
            )

        user_query = await db.execute(select(User).where(User.id == session.user_id))
        user = user_query.scalar_one_or_none()

        if not user:
            return JSONResponse(
                status_code=404,
                content={"error": "Foydalanuvchi topilmadi"}
            )

        joined_date = user.created_at.strftime("%d %b, %Y").lstrip("0") if user.created_at else None

        return JSONResponse(
            status_code=200,
            content={
                "promo": user.promo,
                "xp": user.xp,
                "coins": user.scoin,
                "date_joined": joined_date,
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Xatolik: {str(e)}"}
        )


@router.post("/general/update")
async def update_general_settings(
    request: Request,
    language: str = Form(None),
    theme: str = Form(None),
    background: str = Form(None),
    db: AsyncSession = Depends(get_db),
    access_token: Annotated[str | None, Cookie()] = None
):
    """Foydalanuvchi umumiy sozlamalarini yangilash"""
    if not access_token:
        return JSONResponse(
            status_code=401,
            content={"error": "Avtentifikatsiya talab qilinadi"}
        )
    
    try:
        cookie = loads(access_token)
        token = cookie.get("token")
        
        # Token orqali userga kirish
        query = select(UserToken).where(UserToken.token == token)
        result = await db.execute(query)
        session = result.scalar_one_or_none()
        
        if not session:
            return JSONResponse(
                status_code=401,
                content={"error": "Token noto'g'ri yoki eskirgan"}
            )
        
        # Userga kirish
        user_query = await db.execute(select(User).where(User.id == session.user_id))
        user = user_query.scalar_one_or_none()
        
        if not user:
            return JSONResponse(
                status_code=404,
                content={"error": "Foydalanuvchi topilmadi"}
            )
        
        # Sozlamalarni yangilash
        if language and language in ["uz", "ru", "en", "ky", "tk"]:
            user.language = language
        
        if theme and theme in ["light", "dark"]:
            user.theme = theme
        
        if background:
            user.background = background
        
        await db.commit()
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "Sozlamalar muvaffaqiyatli yangilandi",
                "language": user.language,
                "theme": user.theme,
                "background": user.background
            }
        )
    except Exception as e:
        await db.rollback()
        return JSONResponse(
            status_code=500,
            content={"error": f"Xatolik: {str(e)}"}
        )
