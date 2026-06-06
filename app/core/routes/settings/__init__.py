from fastapi import APIRouter
from .general_settings import router as general_router
from .account_settings import router as account_router
from .main_settings import router as main_settings_router

settings = APIRouter(tags=["settings"])

# Routers qo'shish
settings.include_router(main_settings_router)
settings.include_router(general_router)
settings.include_router(account_router)
