from fastapi import APIRouter, Depends, Form, Request, Cookie
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from json import loads, dumps
from typing import Annotated
from ...database import get_db
from ...models import User, UserToken
import bcrypt

router = APIRouter()


@router.get("/account")
async def get_account_settings(
    db: AsyncSession = Depends(get_db),
    access_token: Annotated[str | None, Cookie()] = None
):
    """Akkaunt sozlamalarini olish"""
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
                "created_at": str(user.created_at),
                "verified": True  # Keyinchalik email verification qilsak bo'ladi
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Xatolik: {str(e)}"}
        )


@router.post("/account/change-password")
async def change_password(
    old_password: str = Form(...),
    new_password: str = Form(...),
    confirm_password: str = Form(...),
    db: AsyncSession = Depends(get_db),
    access_token: Annotated[str | None, Cookie()] = None
):
    """Parolni o'zgartiruvi"""
    if not access_token:
        return JSONResponse(
            status_code=401,
            content={"error": "Avtentifikatsiya talab qilinadi"}
        )
    
    try:
        # Parol validatsiyasi
        if len(new_password) < 8:
            return JSONResponse(
                status_code=400,
                content={"error": "Yangi parol kamida 8 ta belgidan iborat bo'lishi kerak"}
            )
        
        if new_password != confirm_password:
            return JSONResponse(
                status_code=400,
                content={"error": "Parollar mos kelmadi"}
            )
        
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
        
        # Eski parolni tekshirish
        if not bcrypt.checkpw(old_password.encode('utf-8'), user.password.encode('utf-8')):
            return JSONResponse(
                status_code=400,
                content={"error": "Eski parol noto'g'ri"}
            )
        
        # Yangi parol hesh qilish va saqlash
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        user.password = hashed_password.decode('utf-8')
        
        await db.commit()
        
        return JSONResponse(
            status_code=200,
            content={"message": "Parol muvaffaqiyatli o'zgartirildi"}
        )
    
    except Exception as e:
        await db.rollback()
        return JSONResponse(
            status_code=500,
            content={"error": f"Xatolik: {str(e)}"}
        )


@router.post("/account/update-profile")
async def update_profile(
    username: str = Form(None),
    db: AsyncSession = Depends(get_db),
    access_token: Annotated[str | None, Cookie()] = None
):
    """Profil ma'lumotlarini yangilash"""
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
        
        # Username yangilash (agar berilgan bo'lsa)
        if username and username != user.username:
            # Username tekshirish - allaqachon mavjudmi?
            existing_user = await db.execute(
                select(User).where(User.username == username)
            )
            if existing_user.scalar_one_or_none():
                return JSONResponse(
                    status_code=400,
                    content={"error": "Bu foydalanuvchi nomi band"}
                )
            
            user.username = username
        
        await db.commit()
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "Profil muvaffaqiyatli yangilandi",
                "username": user.username
            }
        )
    
    except Exception as e:
        await db.rollback()
        return JSONResponse(
            status_code=500,
            content={"error": f"Xatolik: {str(e)}"}
        )


@router.post("/account/verify-email")
async def verify_account(
    verification_code: str = Form(...),
    db: AsyncSession = Depends(get_db),
    access_token: Annotated[str | None, Cookie()] = None
):
    """Akkauntni tekshiruvi (EMAIL/SMS kod orqali)"""
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
        
        # TODOD: Email/SMS orqali tekshiruv kodini yuborish va tekshirish logikasi
        # Hozircha placeholder
        if len(verification_code) < 4:
            return JSONResponse(
                status_code=400,
                content={"error": "Tekshiruv kodi noto'g'ri"}
            )
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "Akkaunt muvaffaqiyatli tekshirildi",
                "verified": True
            }
        )
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Xatolik: {str(e)}"}
        )


@router.post("/account/delete")
async def delete_account(
    password: str = Form(...),
    db: AsyncSession = Depends(get_db),
    access_token: Annotated[str | None, Cookie()] = None
):
    """Akkauntni o'chiruvi"""
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
        
        # Parolni tekshirish
        if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return JSONResponse(
                status_code=400,
                content={"error": "Parol noto'g'ri"}
            )
        
        # Foydalanuvchining barcha tokenlarini olib tashlaymiz
        await db.execute(delete(UserToken).where(UserToken.user_id == user.id))
        
        # Akkauntni o'chirish
        await db.delete(user)
        await db.commit()
        
        return JSONResponse(
            status_code=200,
            content={"message": "Akkaunt muvaffaqiyatli o'chirildi"}
        )
    
    except Exception as e:
        await db.rollback()
        return JSONResponse(
            status_code=500,
            content={"error": f"Xatolik: {str(e)}"}
        )
