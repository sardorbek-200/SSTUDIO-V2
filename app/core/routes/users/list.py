from fastapi import APIRouter, Request, Depends, Cookie, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from ...config import templates_path
from ...database import get_db
from ...models import User, UserToken, Status
from json import loads

router = APIRouter()
templates = Jinja2Templates(directory=templates_path)

async def get_authenticated_user(request: Request, db: AsyncSession, access_token: Annotated[str | None, Cookie()] = None):
    if not access_token:
        return None
    try:
        cookie = loads(access_token)
        token_str = cookie.get("token")
    except Exception:
        return None
    if not token_str:
        return None
    query = select(UserToken).where(UserToken.token == token_str)
    result = await db.execute(query)
    session = result.scalar_one_or_none()
    if not session or session.ip_address != request.client.host:
        return None
    user_query = await db.execute(select(User).where(User.id == session.user_id))
    return user_query.scalar_one_or_none()


@router.get("/", response_class=HTMLResponse)
async def users_page(
    request: Request,
    page: int = 1,
    db: AsyncSession = Depends(get_db),
    access_token: Annotated[str | None, Cookie()] = None,
):
    page = max(page, 1)
    page_size = 20

    current_user = await get_authenticated_user(request, db, access_token)
    status = "AUTHORIZED" if current_user else "UNAUTHORIZED"
    username = current_user.username if current_user else None

    total_users_query = await db.execute(select(func.count(User.id)))
    total_users = total_users_query.scalar() or 0
    total_pages = (total_users + page_size - 1) // page_size
    offset = (page - 1) * page_size

    users_query = await db.execute(
        select(User)
        .order_by(User.xp.desc())
        .offset(offset)
        .limit(page_size)
    )
    users = users_query.scalars().all()

    return templates.TemplateResponse(
        name="users.html",
        request=request,
        context={
            "request": request,
            "status": status,
            "username": username,
            "title": "Foydalanuvchilar",
            "background": current_user.background if current_user else "/static/images/default_bg.png",
            "users": users,
            "page": page,
            "total_pages": total_pages,
            "total_users": total_users,
            "page_size": page_size,
            "offset": offset,
        },
    )


@router.get("/{id}", response_class=HTMLResponse)
async def user_detail(
    request: Request,
    id: int,
    db: AsyncSession = Depends(get_db),
    access_token: Annotated[str | None, Cookie()] = None,
):
    if not access_token:
        return RedirectResponse(url="/auth/sign-in", status_code=302)

    try:
        cookie = loads(access_token)
        token_str = cookie.get("token")
    except Exception:
        return RedirectResponse(url="/auth/sign-in", status_code=302)

    query = select(UserToken).where(UserToken.token == token_str)
    result = await db.execute(query)
    session = result.scalar_one_or_none()

    if not session or session.ip_address != request.client.host:
        return RedirectResponse(url="/auth/sign-in", status_code=302)

    user_query = await db.execute(select(User).where(User.id == session.user_id))
    user = user_query.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    target_query = await db.execute(select(User).where(User.id == id))
    target_user = target_query.scalar_one_or_none()
    if not target_user:
        raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")

    status_query = await db.execute(select(Status).where(Status.user_id == target_user.id))
    status = status_query.scalar_one_or_none()

    response = templates.TemplateResponse(
        request=request,
        name="user_for_iframe.html",
        context={
            "request": request,
            "user": target_user,
            "status": status,
        },
    )
    return response
