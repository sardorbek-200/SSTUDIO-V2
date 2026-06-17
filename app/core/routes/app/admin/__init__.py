from fastapi import APIRouter, Depends, Request, Cookie, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from ....database import get_db
from ....config import templates_path
from fastapi.templating import Jinja2Templates
from json import loads
from sqlalchemy import select
from app.core.models import UserToken, User
from .check import checkadmin
from typing import Annotated
template = Jinja2Templates(directory=templates_path)

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/", response_class=HTMLResponse)
async def admin_dashboard(
    request: Request,
    db=Depends(get_db),
    access_token: Annotated[str, Cookie()] = None
):
    if access_token is None:
        return RedirectResponse(url="/auth/sign-in", status_code=302)

    try:
        session = loads(access_token)
        token = session.get("token")
    except Exception:
        return RedirectResponse(url="/auth/sign-in", status_code=302)

    user_token_query = await db.execute(select(UserToken).where(UserToken.token == token))
    user_token = user_token_query.scalar_one_or_none()
    if not user_token:
        return RedirectResponse(url="/auth/sign-in", status_code=302)

    user_query = await db.execute(select(User).where(User.id == user_token.user_id))
    user = user_query.scalar_one_or_none()
    if not user:
        return RedirectResponse(url="/auth/sign-in", status_code=302)

    is_admin = await checkadmin(db, user)
    if not is_admin:
        raise HTTPException(status_code=403, detail="Siz admin emassiz")

    response = template.TemplateResponse(
        name="admin/admin.html",
        request=request,
        context={
            "request": request,
            "status": "AUTHORIZED",
            "user": user.username,
            "username": user.username,
            "title": "Admin Panel",
            "background": user.background,
            "admin": is_admin
        }
    )
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response


@router.get("/users", response_class=HTMLResponse)
async def admin_users(
    request: Request,
    db=Depends(get_db),
    access_token: Annotated[str, Cookie()] = None,
):
    if access_token is None:
        return RedirectResponse(url="/auth/sign-in", status_code=302)

    try:
        session = loads(access_token)
        token = session.get("token")
    except Exception:
        return RedirectResponse(url="/auth/sign-in", status_code=302)

    user_token_query = await db.execute(select(UserToken).where(UserToken.token == token))
    user_token = user_token_query.scalar_one_or_none()
    if not user_token:
        return RedirectResponse(url="/auth/sign-in", status_code=302)

    current_user_query = await db.execute(select(User).where(User.id == user_token.user_id))
    current_user = current_user_query.scalar_one_or_none()
    if not current_user:
        return RedirectResponse(url="/auth/sign-in", status_code=302)

    is_admin = await checkadmin(db, current_user)
    if not is_admin:
        raise HTTPException(status_code=403, detail="Siz admin emassiz")

    users_query = await db.execute(select(User).order_by(User.id.desc()))
    users = users_query.scalars().all()

    response = template.TemplateResponse(
        name="admin/users.html",
        request=request,
        context={
            "request": request,
            "status": "AUTHORIZED",
            "username": current_user.username,
            "title": "Admin - Foydalanuvchilar",
            "background": current_user.background,
            "admin": is_admin,
            "users": users,
        }
    )
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response
