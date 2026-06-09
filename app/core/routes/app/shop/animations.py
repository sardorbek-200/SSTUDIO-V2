from fastapi import APIRouter, Request, Depends, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ....config import templates_path
from ....database import get_db
from app.core.models import User, ShopAnimation
from .utils import get_authenticated_user

router = APIRouter(prefix="/animations", tags=["shop-animations"])
templates = Jinja2Templates(directory=templates_path)

async def _build_animation_context(request: Request, user, animation_items, message=None, error=None):
    return {
        "request": request,
        "title": "Animatsiya bozori",
        "background": user.background or "/static/images/default_bg.png",
        "status": "AUTHORIZED",
        "username": user.username,
        "animation_items": animation_items,
        "scoin": user.scoin,
        "message": message,
        "error": error,
    }

@router.get("/", response_class=HTMLResponse)
async def animation_market(
    request: Request,
    db: AsyncSession = Depends(get_db),
    access_token: str | None = Cookie(default=None),
):
    user = await get_authenticated_user(access_token, db)
    if user is None:
        return RedirectResponse(url="/auth/sign-in", status_code=302)

    animation_query = select(ShopAnimation).where(ShopAnimation.is_active == True).order_by(ShopAnimation.price)
    animation_result = await db.execute(animation_query)
    animation_items = animation_result.scalars().all()

    return templates.TemplateResponse(
        name="shop/animations.html",
        request=request,
        context={**await _build_animation_context(request, user, animation_items), "user_id": user.id},
    )
