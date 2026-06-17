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
# Har 30 minutda bazani eski tokenlardan tozalash funksiyasi
async def cleanup_expired_sessions(db: AsyncSession):
    threshold = datetime.now() - timedelta(minutes=30)
    query = delete(UserToken).where(UserToken.last_activity < threshold)
    await db.execute(query)
    await db.commit()
    await sleep(15 * 60)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Server yoqilganda
    async with AsyncSessionLocal() as db:
        # Funksiyaga db argumentini beramiz
        task = create_task(cleanup_expired_sessions(db=db)) 
        yield
    # Shutdown: Server o'chirilganda
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
