from colorama import init
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from ...config import Settings
import asyncio
engine = create_async_engine(Settings.DATABASE_URL,echo=True)

AsyncSessionLocal = async_sessionmaker(
    bind = engine,
    expire_on_commit=False,
    class_=AsyncSession
)

class Base(DeclarativeBase):
    pass

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            if session.in_transaction():
                await session.commit()  # Agar xato bo'lmasa, avtomatik commit qiladi
        except Exception:
            if session.in_transaction():
                await session.rollback()  # Xato bo'lsa, avtomatik rollback qiladi
            raise  # Xatoni FastAPI-ga uzatadi, u esa 500 xatosini ko'rsatadi


async def init_db():
    async with engine.begin() as conn:
        # Bu buyruq barcha modellaringni bazaga avtomatik "tashlaydi"
        await conn.run_sync(Base.metadata.create_all)
