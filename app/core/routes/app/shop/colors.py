from fastapi import APIRouter, Request, Depends, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ....config import templates_path
from ....database import get_db
from app.core.models import User, ShopColor
from .utils import get_authenticated_user

router = APIRouter(prefix="/colors", tags=["shop-colors"])
templates = Jinja2Templates(directory=templates_path)

async def _build_color_context(request: Request, user, color_items, message=None, error=None):
    return {
        "request": request,
        "title": "Rang bozori",
        "background": user.background or "/static/images/default_bg.png",
        "status": "AUTHORIZED",
        "username": user.username,
        "color_items": color_items,
        "scoin": user.scoin,
        "message": message,
        "error": error,
    }

@router.get("/", response_class=HTMLResponse)
async def color_market(
    request: Request,
    db: AsyncSession = Depends(get_db),
    access_token: str | None = Cookie(default=None),
):
    user = await get_authenticated_user(access_token, db)
    if user is None:
        return RedirectResponse(url="/auth/sign-in", status_code=302)

    color_query = select(ShopColor).where(ShopColor.is_active == True).order_by(ShopColor.price)
    color_result = await db.execute(color_query)
    color_items = color_result.scalars().all()

    return templates.TemplateResponse(
        name="shop/colors.html",
        request=request,
        context={**await _build_color_context(request, user, color_items), "user_id": user.id},
    )
