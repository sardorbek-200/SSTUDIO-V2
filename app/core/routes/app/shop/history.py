from fastapi import APIRouter, Request, Depends, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ....config import templates_path
from ....database import get_db
from .utils import get_authenticated_user
from app.core.models import ShopHistory

router = APIRouter(prefix="/history", tags=["shop-history"])
templates = Jinja2Templates(directory=templates_path)

@router.get("/", response_class=HTMLResponse)
async def shop_history(
    request: Request,
    db: AsyncSession = Depends(get_db),
    access_token: str | None = Cookie(default=None),
):
    user = await get_authenticated_user(access_token, db)
    if user is None:
        return RedirectResponse(url="/auth/sign-in", status_code=302)

    history_result = await db.execute(select(ShopHistory).where(ShopHistory.user_id == user.id).order_by(ShopHistory.created_at.desc()))
    history_items = history_result.scalars().all()

    return templates.TemplateResponse(
        name="shop/history.html",
        request=request,
        context={
            "request": request,
            "title": "Shop tarixi",
            "background": user.background or "/static/images/default_bg.png",
            "status": "AUTHORIZED",
            "username": user.username,
            "history_items": history_items,
        },
    )
