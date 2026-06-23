from fastapi import APIRouter,Request,Depends,Cookie
from app.core.models import UserToken, User, Admin
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
from ...config import templates_path
from typing import Annotated
from ...database import get_db
from json import loads
from sqlalchemy import select
from .quizer import router as quizer_router
from .shop import router as shop_router
from .admin.check import checkadmin
router = APIRouter(prefix="/app", tags=["app"])
templates = Jinja2Templates(directory=templates_path)
router.include_router(quizer_router)
router.include_router(shop_router)
@router.get("/", response_class=HTMLResponse)
async def apps(request: Request, db: UserToken = Depends(get_db), access_token: Annotated[str | None, Cookie()] = None):
    if access_token is None:
        return RedirectResponse(url="/auth/sign-in", status_code=302)
    session = loads(access_token)
    user_query = await db.execute(select(UserToken).where(UserToken.token == session.get("token")))
    user = user_query.scalar_one_or_none()
    if not user:
        return RedirectResponse(url="/auth/sign-in",status_code=302)
    user_query = await db.execute(select(User).where(User.id == user.user_id))
    user = user_query.scalar_one_or_none()
    is_admin = await checkadmin(db,user)
    response = templates.TemplateResponse(name = "apps.html",request= request, context = {"request": request, "status":"AUTHORIZED","user": user.username,"username":user.username,"title": "Ilovalar","background":user.background,"scoin":user.scoin, "admin":is_admin})
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response