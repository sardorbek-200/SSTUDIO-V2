from fastapi import APIRouter, Request, Depends, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ....config import templates_path
from ....database import get_db
from app.core.models import User, ShopAnimation
from .utils import get_authenticated_user

router = APIRouter(prefix="/avatars", tags=["shop-avatars"])
templates = Jinja2Templates(directory=templates_path)

async def _build_avatar_context(request: Request, user, avatar_items, message=None, error=None):
    return {
        "request": request,
        "title": "Profil rasm bozori",
        "background": user.background or "/static/images/default_bg.png",
        "status": "AUTHORIZED",
        "username": user.username,
        "avatar_items": avatar_items,
        "scoin": user.scoin,
        "message": message,
        "error": error,
    }

@router.get("/", response_class=HTMLResponse)
async def avatar_market(
    request: Request,
    db: AsyncSession = Depends(get_db),
    access_token: str | None = Cookie(default=None),
):
    user = await get_authenticated_user(access_token, db)
    if user is None:
        return RedirectResponse(url="/auth/sign-in", status_code=302)

    avatar_query = select(ShopAnimation).where(ShopAnimation.is_active == True).order_by(ShopAnimation.price)
    avatar_result = await db.execute(avatar_query)
    avatar_items = avatar_result.scalars().all()

    return templates.TemplateResponse(
        name="shop/avatars.html",
        request=request,
        context={**await _build_avatar_context(request, user, avatar_items), "user_id": user.id},
    )
