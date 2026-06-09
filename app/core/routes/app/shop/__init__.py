from fastapi import APIRouter, Request, Depends, Cookie, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ....config import templates_path
from ....database import get_db
from app.core.models import (
    User,
    Status,
    ShopRank,
    ShopAnimation,
    ShopColor,
    ShopBackground,
    log_scoin_transaction,
)
from .utils import get_authenticated_user
from .rank import router as rank_router
from .backgrounds import router as background_router
from .colors import router as colors_router
from .avatars import router as avatars_router
from .animations import router as animations_router
from .history import router as history_router
from .products import router as products_router
from .cart import router as cart_router
from .orders import router as orders_router

router = APIRouter(prefix="/shop", tags=["shop"])
templates = Jinja2Templates(directory=templates_path)
router.include_router(rank_router)
router.include_router(background_router)
router.include_router(colors_router)
router.include_router(avatars_router)
router.include_router(animations_router)
router.include_router(history_router)
router.include_router(products_router)
router.include_router(cart_router)
router.include_router(orders_router)

@router.get("/", response_class=HTMLResponse)
async def shop_home(
    request: Request,
    db: AsyncSession = Depends(get_db),
    access_token: str | None = Cookie(default=None),
):
    user = await get_authenticated_user(access_token, db)
    if user is None:
        return RedirectResponse(url="/auth/sign-in", status_code=302)

    return templates.TemplateResponse(
        name = "shop/index.html",
        request=request,
        context={
            "request": request,
            "title": "Shop bozori",
            "background": user.background or "/static/images/default_bg.png",
            "status": "AUTHORIZED",
            "username": user.username,
            "scoin": user.scoin,
        },
    )


@router.post("/buy")
async def purchase_item(
    item_type: str = Form(...),
    item_id: int = Form(...),
    user_id: int = Form(...),
    db: AsyncSession = Depends(get_db),
):
    user_result = await db.execute(select(User).where(User.id == user_id))
    user = user_result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User topilmadi.")

    item_query = None
    item = None
    if item_type == "rank":
        item_query = select(ShopRank).where(ShopRank.id == item_id, ShopRank.is_active == True)
    elif item_type == "animation":
        item_query = select(ShopAnimation).where(ShopAnimation.id == item_id, ShopAnimation.is_active == True)
    elif item_type == "color":
        item_query = select(ShopColor).where(ShopColor.id == item_id, ShopColor.is_active == True)
    elif item_type == "background":
        item_query = select(ShopBackground).where(ShopBackground.id == item_id, ShopBackground.is_active == True)
    else:
        raise HTTPException(status_code=400, detail="Noto'g'ri item_type.")

    item_result = await db.execute(item_query)
    item = item_result.scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=400, detail="Item topilmadi yoki faol emas.")

    if user.scoin < item.price:
        raise HTTPException(status_code=400, detail="Scoin yetarli emas!")

    user.scoin -= item.price
    description = f"{item_type.capitalize()} sotib olindi: {getattr(item, 'name', str(item_id))}"
    await log_scoin_transaction(user_id=user.id, amount=-item.price, description=description, db=db)

    status_result = await db.execute(select(Status).where(Status.user_id == user.id))
    status = status_result.scalar_one_or_none()
    if status is None:
        status = Status(user_id=user.id, rank="", color="", animation="")
        db.add(status)
        await db.flush()

    if item_type == "background":
        user.background = item.picture
    elif item_type == "rank":
        status.rank = item.name
        status.color = getattr(item, "rank_color", status.color)
    elif item_type == "animation":
        status.animation = getattr(item, "css_code", status.animation)
    elif item_type == "color":
        status.color = getattr(item, "name_color", status.color)

    await db.commit()

    response_data = {
        "status": "success",
        "message": "Sotib olish muvaffaqiyatli amalga oshirildi.",
        "new_balance": user.scoin,
    }
    if item_type == "background":
        response_data["new_bg"] = item.picture

    return JSONResponse(response_data)
