import logging
from typing import Annotated
from json import loads
from fastapi import APIRouter, Request, Depends, Cookie
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

# Aiogram 3.x importlari
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Update
from contextlib import asynccontextmanager
# Loyihangiz ichki modullari (o'z yo'lingizga moslang)
from app.core.database import get_db
from app.core.models import UserToken, TelegramAccount
from ....config import TG_TOKEN  # Sening configingdagi bot tokeni

# Loggingni sozlaymiz (xatoliklarni konsolda ko'rish uchun)
logging.basicConfig(level=logging.INFO)

# 1. Bot va Dispatcher obyektlarini yaratamiz
bot = Bot(token=TG_TOKEN)
dp = Dispatcher()

@asynccontextmanager
async def lifespan(app: APIRouter):
    # --- LOYIHA ISHGA TUSHHGANDA (STARTUP) ---
    # Sening loyihang ishlayotgan jonli domen yoki ngrok manzili
    # Buni .env faylida saqlash tavsiya etiladi
    DOMAIN_URL = "https://unsponsored-paulita-shakingly.ngrok-free.dev/app"
    
    print("🚀 FastAPI ishga tushmoqda... Telegram Webhook sozlanmoqda...")
    await set_telegram_webhook(DOMAIN_URL)
    
    yield  # Shu joyda FastAPI to'xtab, so'rovlarni qabul qilishni boshlaydi
    
    # --- LOYIHA O'CHGANDA (SHUTDOWN) ---
    print("🛑 FastAPI o'chmoqda... Telegram Webhook tozalanmoqda...")
    await bot.delete_webhook()

# Webhook routerini yaratamiz
router = APIRouter(prefix="/telegram", tags=["Telegram Webhook"], lifespan=lifespan)

# --------------------------------------------------------------------------
# 🤖 AIOGRAM: BOTGA /START TOKEN KELGANDAGI MANTIQ
# --------------------------------------------------------------------------
@dp.message(CommandStart())
async def bot_start_handler(message: types.Message, command: CommandObject):
    token_arg = command.args  # URL'dan kelgan start={session.token} qismi
    
    if not token_arg:
        await message.answer(
            "👋 Xush kelibsiz!\n\nBotni Quizer profilingizga bog'lash uchun ilova sahifasidagi 'Davom etish' tugmasini bosing."
        )
        return

    # Webhook orqali kelgan so'rovda DB sessiyasini ochish uchun Context Manager ishlatamiz
    # Eslatma: get_db asinxron generator bo'lgani uchun undan asinxron sessiyani ajratib olamiz
    from app.core.database import get_db
    async for db in get_db():
        try:
            # 1. Kelgan token bazadagi UserToken ichida bormi-yo'qligini tekshiramiz
            query = select(UserToken).where(UserToken.token == token_arg)
            result = await db.execute(query)
            session_data = result.scalar_one_or_none()

            if not session_data:
                await message.answer("❌ Xatolik: Havola eskirgan yoki xavfsizlik tokeni noto'g'ri!")
                return

            # 2. Ushbu user_id bilan allaqachon telegram akkaunt bog'langanmi tekshiramiz
            tg_query = select(TelegramAccount).where(TelegramAccount.user_id == session_data.user_id)
            tg_result = await db.execute(tg_query)
            existing_tg = tg_result.scalar_one_or_none()

            if existing_tg:
                # Agar bor bo'lsa, ma'lumotlarini shunchaki yangilab, faollashtiramiz
                existing_tg.tg_id = str(message.from_user.id)
                existing_tg.username = message.from_user.username
                existing_tg.first_name = message.from_user.first_name
                existing_tg.last_name = message.from_user.last_name
                existing_tg.is_active = True
                
                await message.answer("✅ Sizning Telegram akkauntingiz muvaffaqiyatli yangilandi va bog'landi!")
            else:
                # 3. Agar mutlaqo yangi bo'lsa, telegram_accounts jadvaliga saqlaymiz
                new_tg_account = TelegramAccount(
                    user_id=session_data.user_id,
                    tg_id=str(message.from_user.id),
                    username=message.from_user.username,
                    first_name=message.from_user.first_name,
                    last_name=message.from_user.last_name,
                    is_active=True
                )
                db.add(new_tg_account)
                
                await message.answer(
                    f"🎉 Tabriklaymiz, {message.from_user.first_name}!\n\n"
                    f"Akkauntingiz Quizer tizimiga muvaffaqiyatli ulandi. "
                    f"Endi brauzerga qaytib testlarni davom ettirishingiz mumkin."
                )

            # O'zgarishlarni bazaga saqlaymiz
            await db.commit()
            
        except Exception as e:
            await db.rollback()
            logging.error(f"Telegram webhook tranzaksiya xatoligi: {str(e)}")
            await message.answer("⚙️ Tizimda xatolik yuz berdi. Birozdan so'ng qayta urinib ko'ring.")
        break


# --------------------------------------------------------------------------
# 🌐 FASTAPI: TELEGRAM WEBHOOK ENDPOINTI
# --------------------------------------------------------------------------
# Telegram serverlari sening saytingga JSON yuboradigan URL manzil
@router.post("/webhook")
async def telegram_webhook_endpoint(request: Request):
    try:
        # Telegram yuborgan JSON ma'lumotni o'qiymiz
        updater_json = await request.json()
        
        # Uni Aiogram tushunadigan Update obyektiga aylantiramiz
        update = Update.model_validate(updater_json, context={"bot": bot})
        
        # Aiogram dispetcheriga so'rovni topshiramiz, u start_handlerga otib yuboradi
        await dp.feed_update(bot, update)
        
        return JSONResponse(status_code=200, content={"status": "ok"})
    except Exception as e:
        logging.error(f"Webhook error: {str(e)}")
        return JSONResponse(status_code=500, content={"error": str(e)})


# --------------------------------------------------------------------------
# 🛠️ STARTUP: WEBHOOK MANZILINI TELEGRAMGA RO'YXATDAN O'TKAZISH
# --------------------------------------------------------------------------
# Loyihang ishga tushganda (Lifespan yoki @app.on_event("startup")) orqali chaqiriladi
async def set_telegram_webhook(domain_url: str):
    """
    domain_url: Sening loyihang ishlayotgan domen (Masalan: https://api.seningdomening.uz)
    """
    webhook_url = f"{domain_url}/quizer/telegram/webhook"
    logging.info(f"Setting telegram webhook to: {webhook_url}")
    await bot.set_webhook(url=webhook_url)