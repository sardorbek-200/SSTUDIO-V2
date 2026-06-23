import os
import shutil
from fastapi import APIRouter, Depends, Request, Cookie, HTTPException, Form, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ....database import get_db
from ....config import templates_path
from app.core.models import ShopRank, ShopBackground, ShopColor, ShopAnimation
from .check import checkadmin, get_admin_user

template = Jinja2Templates(directory=templates_path)
router = APIRouter(tags=["admin_shop"])

UPLOAD_DIR = os.path.join("v2", "static", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 🌐 ASOSIY SAHIFA
@router.get("/shop", response_class=HTMLResponse)
async def admin_shop_page(
    request: Request,
    db: AsyncSession = Depends(get_db),
    access_token: Annotated[str | None, Cookie()] = None
):
    current_user = await get_admin_user(db, access_token)
    if not current_user or not await checkadmin(db, current_user):
        return RedirectResponse(url="/auth/sign-in", status_code=302)

    ranks = (await db.execute(select(ShopRank))).scalars().all()
    backgrounds = (await db.execute(select(ShopBackground))).scalars().all()
    colors = (await db.execute(select(ShopColor))).scalars().all()
    animations = (await db.execute(select(ShopAnimation))).scalars().all()

    # MANA SHU QISM O'ZGARTIRILDI (Kalit so'zlar bilan aniq berildi)
    return template.TemplateResponse(
        request=request,
        name="admin/shop.html",
        context={
            "request": request, 
            "username": current_user.username, 
            "ranks": ranks, 
            "title":"SHOP tizimi",
            "backgrounds": backgrounds, 
            "colors": colors, 
            "animations": animations,
            "background": current_user.background,
            "status":"AUTHORIZED"
        }
    )
# --------------------------------------------------------------------------
# ⚡ ALOHIDA API'LAR (YANGI QO'SHISH UCHUN)
# --------------------------------------------------------------------------

# 1. RANK QO'SHISH API
@router.post("/shop/add/rank")
async def add_rank(
    name: str = Form(...), price: int = Form(...), description: str = Form(""),
    rank_color: str = Form("#ffffff"), db: AsyncSession = Depends(get_db),
    access_token: Annotated[str | None, Cookie()] = None
):
    user = await get_admin_user(db, access_token)
    if not user or not await checkadmin(db, user): return JSONResponse({"status": "error", "message": "Ruxsat yo'q"}, 403)
    
    try:
        new_item = ShopRank(name=name, description=description, price=price, rank_color=rank_color, is_active=True)
        db.add(new_item)
        await db.commit()
        return {"status": "success", "message": "Rank muvaffaqiyatli qo'shildi!"}
    except Exception as e:
        await db.rollback()
        return JSONResponse({"status": "error", "message": str(e)}, 500)

# 2. BACKGROUND QO'SHISH API (RASM YUKLASH)
@router.post("/shop/add/background")
async def add_background(
    name: str = Form(...), price: int = Form(...), description: str = Form(""),
    file: UploadFile = File(...), db: AsyncSession = Depends(get_db),
    access_token: Annotated[str | None, Cookie()] = None
):
    user = await get_admin_user(db, access_token)
    if not user or not await checkadmin(db, user): return JSONResponse({"status": "error", "message": "Ruxsat yo'q"}, 403)
    
    try:
        file_url = "/static/images/default_bg.png"
        if file and file.filename:
            file_path = os.path.join(UPLOAD_DIR, file.filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            file_url = f"/uploads/{file.filename}"

        new_item = ShopBackground(name=name, description=description, price=price, picture=file_url, is_active=True)
        db.add(new_item)
        await db.commit()
        return {"status": "success", "message": "Fon rasmi muvaffaqiyatli yuklandi!"}
    except Exception as e:
        await db.rollback()
        return JSONResponse({"status": "error", "message": str(e)}, 500)

# 3. COLOR (NIK RANGI) QO'SHISH API
@router.post("/shop/add/color")
async def add_color(
    name: str = Form(...), price: int = Form(...), description: str = Form(""),
    color_code: str = Form("#ffffff"), db: AsyncSession = Depends(get_db),
    access_token: Annotated[str | None, Cookie()] = None
):
    user = await get_admin_user(db, access_token)
    if not user or not await checkadmin(db, user): return JSONResponse({"status": "error", "message": "Ruxsat yo'q"}, 403)

    try:
        new_item = ShopColor(name=name, description=description, price=price, color=color_code, is_active=True)
        db.add(new_item)
        await db.commit()
        return {"status": "success", "message": "Nik rangi muvaffaqiyatli qo'shildi!"}
    except Exception as e:
        await db.rollback()
        return JSONResponse({"status": "error", "message": str(e)}, 500)

# 4. ANIMATION QO'SHISH API
@router.post("/shop/add/animation")
async def add_animation(
    name: str = Form(...), price: int = Form(...), description: str = Form(""),
    css_code: str = Form(...), db: AsyncSession = Depends(get_db),
    access_token: Annotated[str | None, Cookie()] = None
):
    user = await get_admin_user(db, access_token)
    if not user or not await checkadmin(db, user): return JSONResponse({"status": "error", "message": "Ruxsat yo'q"}, 403)

    try:
        new_item = ShopAnimation(name=name, description=description, price=price, css_code=css_code, is_active=True)
        db.add(new_item)
        await db.commit()
        return {"status": "success", "message": "Animatsiya muvaffaqiyatli qo'shildi!"}
    except Exception as e:
        await db.rollback()
        return JSONResponse({"status": "error", "message": str(e)}, 500)


# --------------------------------------------------------------------------
# ❌ O'CHIRISH API (YAGONA, CHUNKI FAKAT ID KETADI)
# --------------------------------------------------------------------------
@router.post("/shop/delete/{item_type}/{item_id}")
async def delete_shop_item(
    item_type: str, item_id: int, db: AsyncSession = Depends(get_db),
    access_token: Annotated[str | None, Cookie()] = None
):
    user = await get_admin_user(db, access_token)
    if not user or not await checkadmin(db, user): return JSONResponse({"status": "error", "message": "Ruxsat yo'q"}, 403)

    model_mapping = {"rank": ShopRank, "background": ShopBackground, "color": ShopColor, "animation": ShopAnimation}
    t = item_type.lower()
    
    if t not in model_mapping: return JSONResponse({"status": "error", "message": "Xato tur"}, 400)

    try:
        model = model_mapping[t]
        query = await db.execute(select(model).where(model.id == item_id))
        item = query.scalar_one_or_none()
        if not item: return JSONResponse({"status": "error", "message": "Topilmadi"}, 404)

        await db.delete(item)
        await db.commit()
        return {"status": "success", "message": "O'chirildi"}
    except Exception as e:
        await db.rollback()
        return JSONResponse({"status": "error", "message": str(e)}, 500)