from contextlib import asynccontextmanager
from app.core.config import Settings
from fastapi import FastAPI
from app.core.routes.main_routes import router as main_router
from app.core.routes.auth_routes import auth
from app.core.routes.settings import settings
from app.core.routes.app import router as app_router
from app.core.routes.users import router as users_router
from app.core.routes.app.admin import router as admin_router
from app.core.database import get_db
from app.core.models import UserToken
from datetime import datetime, timedelta
from sqlalchemy import delete
from asyncio import sleep, create_task
from sqlalchemy.ext.asyncio import AsyncSession
from .core.database import AsyncSessionLocal
from fastapi.staticfiles import StaticFiles
import asyncio
# Har 30 minutda bazani eski tokenlardan tozalash funksiyasi
# O'zingning bazang va modelingni import qilib olasan:
# from ....database import AsyncSessionLocal 
# from ....models import UserToken

async def cleanup_expired_sessions():
    # Cheksiz sikl — server o'chguncha tinmay aylanadi
    while True:
        try:
            # Har safar tozalash uchun yangi, qisqa muddatli baza aloqasini ochamiz
            async with AsyncSessionLocal() as db:
                threshold = datetime.now() - timedelta(hours=10)
                query = delete(UserToken).where(UserToken.created_at < threshold)
                
                result = await db.execute(query)
                await db.commit()
                
                print(f"[{datetime.now()}] Eski sessiyalar tozalandi!")
                
        except Exception as e:
            # Agar bazada biror xato bo'lsa, server o'chib qolmasligi uchun
            print(f"Tozalashda xatolik: {e}")
            
        # Mana shu yerda 15 minut (15 * 60 sekund) kutadi va keyin tepaga qaytadi
        await asyncio.sleep(15 * 60)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Server yoqilganda fonda cheksiz vazifani boshlaymiz
    # Endi db ni argument qilib berish shart emas, funksiyani o'zi ochadi
    task = asyncio.create_task(cleanup_expired_sessions()) 
    
    yield  # Shu joyda server ishlayveradi...
    
    # Shutdown: Server o'chirilganda fondagi vazifani to'xtatamiz
    task.cancel()
app = FastAPI(
    title=Settings.PROJECT_NAME,
    description="S-Studio: Yuqori tezlikdagi va xavfsiz backend tizimi",
    version="2.0.0",
    lifespan=lifespan
)



app.include_router(admin_router)
app.include_router(main_router)
app.include_router(auth)
app.include_router(settings)
app.include_router(app_router)
app.include_router(users_router)
