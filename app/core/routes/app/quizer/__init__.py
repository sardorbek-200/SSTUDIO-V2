from json import loads, dumps
import json
from fastapi import APIRouter, Request, Depends, Cookie, HTTPException
from app.core.models import UserToken, User, TelegramAccount , AILearningAnalysis # TelegramAccount modelini qo'shdik
from ....config import templates_path
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated
from sqlalchemy import select
from app.core.database import get_db
from .data import router as data_router
from .create import router as create_router
from .play import router as play_router
from .telegram import router as telegram_router
from .edit import router as edit_router
from .submit_test import router as sub_router
from .results import router as rrouter
from ....config import TELEGRAM_BOT_USERNAME # O'zingizning config yo'lingiz
from sqlalchemy.ext.asyncio import AsyncSession
templates = Jinja2Templates(directory=templates_path)
router = APIRouter(prefix="/quizer", tags=["quizer"])

router.include_router(data_router)
router.include_router(create_router)
router.include_router(play_router)
router.include_router(telegram_router)
router.include_router(edit_router)
router.include_router(sub_router)
router.include_router(rrouter)

@router.get("/", response_class=HTMLResponse)
async def quizer(request: Request, db = Depends(get_db), access_token: Annotated[str | None, Cookie()] = None):
    if not access_token:
        return RedirectResponse(url="/auth/login")
        
    try:
        cookie = loads(access_token)
        token_str = cookie.get("token")
    except Exception:
        return RedirectResponse(url="/auth/login")
        
    query = select(UserToken).where(UserToken.token == token_str)
    result = await db.execute(query)
    session = result.scalar_one_or_none()
    
    if not session:
        return RedirectResponse(url="/auth/login")
        
    client_ip = request.client.host
    if session.ip_address != client_ip:
        return RedirectResponse(url="/auth/login")
        
    user_query = await db.execute(select(User).where(User.id == session.user_id))
    user = user_query.scalar_one_or_none()
    
    if not user:
        raise Exception("User not found")
        
    # --------------------------------------------------------------------------
    # ISH TARTIBI 1-QADAM: Telegram akkaunti ulanganligini tekshirish
    # --------------------------------------------------------------------------
    tg_query = select(TelegramAccount).where(TelegramAccount.user_id == user.id)
    tg_result = await db.execute(tg_query)
    tg_account = tg_result.scalar_one_or_none()
    
    # Agar foydalanuvchi Telegramni hali ulamagan bo'lsa va bu sahifaga majburiy kelayotgan bo'lsa
    # (Sessiyaga qarab, foydalanuvchi "O'tkazib yuborish" tugmasini bosgan bo'lsa, qayta-qayta bezovta qilmaslik mantiqi keyin qo'shiladi)
    # Hozircha birinchi marta kirganda to'g'ridan-to'g'ri bildirishnoma sahifasiga otamiz:
    if not tg_account and request.query_params.get("skip") != "true":
        return RedirectResponse(url="telegram-link")

    response = templates.TemplateResponse(name="quizer/index.html", request=request, context={
        "request": request,
        "user": user.username,
        "username": user.username,
        "title": "Quizer",
        "scoin": user.scoin,
        "lang": "uz",
        "status": "AUTHORIZED",
        "theme": "dark",
        "background": user.background,
    })
    response.set_cookie(key="access_token", value=dumps({"token": session.token}), httponly=True)
    return response


# --------------------------------------------------------------------------
# ISH TARTIBI 2-QADAM: Telegram ulanishini taklif qiluvchi oraliq sahifa
# --------------------------------------------------------------------------
@router.get("/telegram-link", response_class=HTMLResponse)
async def telegram_link_page(request: Request, db = Depends(get_db), access_token: Annotated[str | None, Cookie()] = None):
    if not access_token:
        return RedirectResponse(url="/auth/login")
        
    try:
        cookie = loads(access_token)
        token_str = cookie.get("token")
    except Exception:
        return RedirectResponse(url="/auth/login")
        
    query = select(UserToken).where(UserToken.token == token_str)
    result = await db.execute(query)
    session = result.scalar_one_or_none()
    
    if not session:
        return RedirectResponse(url="/auth/login")
    
    user_query = await db.execute(select(User).where(User.id == session.user_id))
    user = user_query.scalar_one_or_none()

    # Telegram botingiz manzili (masalan: @quizer_bot)
    # Tokenni start parametri sifatida berib yuboramiz: t.me/bot_name?start=token
    
    telegram_bot_url = f"https://t.me/{TELEGRAM_BOT_USERNAME}?start={session.token}"
    return templates.TemplateResponse(name="quizer/telegram_link.html", request=request, context={
        "request": request,
        "title": "Telegram Bildirishnomalari",
        "bot_url": telegram_bot_url,
        "username": user.username if user else "User",
        "background": user.background if user else "/static/images/defualt_bg.png",
        "status": "AUTHORIZED"
    })



import json
import markdown  # 🔥 1. Markdown kutubxonasini import qilamiz
from fastapi import APIRouter, Depends, HTTPException, Request, Cookie
from fastapi.responses import HTMLResponse
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

@router.get("/test/{ai_id}/analysis", response_class=HTMLResponse)
async def view_test_analysis(
    request: Request, 
    ai_id: int, 
    db: AsyncSession = Depends(get_db),
    access_token: str = Cookie(None)
):
    username = "Mehmon"
    background_img = "/static/images/default_bg.png"
    status = "UNAUTHORIZED"

    if access_token:
        try:
            session = json.loads(access_token)
            token_str = session.get("token")
            
            user_token_query = await db.execute(select(UserToken).where(UserToken.token == token_str))
            user_token_obj = user_token_query.scalar_one_or_none()
            
            if user_token_obj:
                user_query = await db.execute(select(User).where(User.id == user_token_obj.user_id))
                user = user_query.scalar_one_or_none()
                
                if user:
                    username = user.username
                    status = "AUTHORIZED"
                    if user.background:
                        background_img = user.background
        except Exception:
            pass

    analysis_query = await db.execute(
        select(AILearningAnalysis).where(AILearningAnalysis.id == ai_id)
    )
    analysis_data = analysis_query.scalar_one_or_none()

    if not analysis_data:
        raise HTTPException(status_code=404, detail="Ushbu test uchun tahlil topilmadi!")

    # 🔥 2. SEHRLI JOYI: Markdown matnini toza HTML ko'rinishiga o'giramiz!
    # Bu yulduzchalarni <strong>, sarlavhalarni <h3> va ro'yxatlarni <ul><li> ga aylantiradi.
    raw_markdown = analysis_data.analysis_text or ""
    html_analysis = markdown.markdown(raw_markdown, extensions=['extra', 'nl2br'])

    try:
        archived_questions = json.loads(analysis_data.analysis_questions) if analysis_data.analysis_questions else []
    except Exception:
        archived_questions = []

    gen_time = analysis_data.generated_at.strftime("%Y-%m-%d %H:%M") if analysis_data.generated_at else "Noma'lum vaqt"

    # 🟢 TO'G'RI VARIANT: context= kalit so'zi aniq yozildi!
    return templates.TemplateResponse(
        name="quizer/test_analysis.html",
        request=request,  # Template nomini aniq ko'rsatdik
        context={                   # 🔥 Kalit so'z shu yerda shart!
            "request": request,
            "analysis_text": html_analysis,
            "questions": archived_questions,
            "username": username,
            "background": background_img,
            "status": status,
            "generated_at": gen_time
        }
    )