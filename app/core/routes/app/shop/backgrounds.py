from fastapi import APIRouter, Request, Depends, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ....config import templates_path
from ....database import get_db
from app.core.models import User, ShopBackground
from .utils import get_authenticated_user

router = APIRouter(prefix="/background", tags=["shop-background"])
templates = Jinja2Templates(directory=templates_path)

async def _build_background_context(request: Request, user, background_items, message=None, error=None):
    return {
        "request": request,
        "title": "Background bozori",
        "background": user.background or "/static/images/default_bg.png",
        "status": "AUTHORIZED",
        "username": user.username,
        "background_items": background_items,
        "scoin": user.scoin,
        "message": message,
        "error": error,
    }

@router.get("/", response_class=HTMLResponse)
async def background_market(
    request: Request,
    db: AsyncSession = Depends(get_db),
    access_token: str | None = Cookie(default=None),
):
    user = await get_authenticated_user(access_token, db)
    if user is None:
        return RedirectResponse(url="/auth/sign-in", status_code=302)

    background_query = select(ShopBackground).where(ShopBackground.is_active == True).order_by(ShopBackground.price)
    background_result = await db.execute(background_query)
    background_items = background_result.scalars().all()

    return templates.TemplateResponse(
        name="shop/background.html",
        request=request,
        context={**await _build_background_context(request, user, background_items), "user_id": user.id},
    )

@router.post("/buy/{item_id}", response_class=HTMLResponse)
async def buy_background(
    request: Request,
    item_id: int,
    db: AsyncSession = Depends(get_db),
    access_token: str | None = Cookie(default=None),
):
    user = await get_authenticated_user(access_token, db)
    if user is None:
        return RedirectResponse(url="/auth/sign-in", status_code=302)

    item_query = select(ShopBackground).where(ShopBackground.id == item_id, ShopBackground.is_active == True)
    item_result = await db.execute(item_query)
    item = item_result.scalar_one_or_none()

    background_query = select(ShopBackground).where(ShopBackground.is_active == True).order_by(ShopBackground.price)
    background_result = await db.execute(background_query)
    background_items = background_result.scalars().all()

    if item is None:
        return templates.TemplateResponse(
            name="shop/background.html",
            request=request,
            context=await _build_background_context(request, user, background_items, error="Ushbu fon topilmadi."),
        )

    if user.scoin < item.price:
        return templates.TemplateResponse(
            name="shop/background.html",
            request=request,
            context=await _build_background_context(request, user, background_items, error="Yetarli scoin yo'q."),
        )

    user.scoin -= item.price
    user.background = item.picture

    db.add(user)
    await db.commit()

    return templates.TemplateResponse(
        name="shop/background.html",
        request=request,
        context={**await _build_background_context(request, user, background_items, message=f"{item.name} muvaffaqiyatli sotib olindi."), "user_id": user.id},
    )
