from fastapi import APIRouter, Request, Depends, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ....config import templates_path
from ....database import get_db
from app.core.models import ShopRank, Status
from .utils import get_authenticated_user

router = APIRouter(prefix="/rank", tags=["shop-rank"])
templates = Jinja2Templates(directory=templates_path)

async def _build_rank_context(request: Request, user, rank_items, message=None, error=None):
    return {
        "request": request,
        "title": "Rank bozori",
        "background": user.background or "/static/images/default_bg.png",
        "status": "AUTHORIZED",
        "username": user.username,
        "rank_items": rank_items,
        "scoin": user.scoin,
        "message": message,
        "error": error,
    }

@router.get("/", response_class=HTMLResponse)
async def rank_market(
    request: Request,
    db: AsyncSession = Depends(get_db),
    access_token: str | None = Cookie(default=None),
):
    user = await get_authenticated_user(access_token, db)
    if user is None:
        return RedirectResponse(url="/auth/sign-in", status_code=302)

    rank_query = select(ShopRank).where(ShopRank.is_active == True).order_by(ShopRank.price)
    rank_result = await db.execute(rank_query)
    rank_items = rank_result.scalars().all()

    return templates.TemplateResponse(
        name="shop/rank.html",
        request=request,
        context={**await _build_rank_context(request, user, rank_items), "user_id": user.id},
    )

@router.post("/buy/{item_id}", response_class=HTMLResponse)
async def buy_rank(
    request: Request,
    item_id: int,
    db: AsyncSession = Depends(get_db),
    access_token: str | None = Cookie(default=None),
):
    user = await get_authenticated_user(access_token, db)
    if user is None:
        return RedirectResponse(url="/auth/sign-in", status_code=302)

    item_query = select(ShopRank).where(ShopRank.id == item_id, ShopRank.is_active == True)
    item_result = await db.execute(item_query)
    item = item_result.scalar_one_or_none()
    rank_query = select(ShopRank).where(ShopRank.is_active == True).order_by(ShopRank.price)
    rank_result = await db.execute(rank_query)
    rank_items = rank_result.scalars().all()

    if item is None:
        return templates.TemplateResponse(
            name="shop/rank.html",
            request=request,
            context=await _build_rank_context(request, user, rank_items, error="Ushbu rank topilmadi."),
        )

    if user.scoin < item.price:
        return templates.TemplateResponse(
            name="shop/rank.html",
            request=request,
            context=await _build_rank_context(request, user, rank_items, error="Yetarli scoin yo'q."),
        )

    user.scoin -= item.price
    result = await db.execute(select(Status).where(Status.user_id == user.id))
    status = result.scalar_one_or_none()
    if status is None:
        status = Status(user_id=user.id)
    status.rank = item.name
    status.picture = item.picture
    status.animation = status.animation if status.animation is not None else ""
    status.color = item.rank_color
    status.name_color = item.name_color

    db.add(user)
    db.add(status)
    await db.commit()

    return templates.TemplateResponse(
        name="shop/rank.html",
        request=request,
        context={**await _build_rank_context(request, user, rank_items, message=f"{item.name} ranki muvaffaqiyatli sotib olindi."), "user_id": user.id},
    )
