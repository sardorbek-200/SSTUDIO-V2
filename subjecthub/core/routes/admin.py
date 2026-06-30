from json import loads, dumps
from typing import Annotated
from fastapi import APIRouter, Request, Depends, Cookie, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import User, UserToken
from ...config import templates_path
from ..database import get_db

from .check import checkadmin
templates = Jinja2Templates(directory=templates_path)

router = APIRouter(prefix="/admin")

@router.get("/", response_class=HTMLResponse)
async def home_page(
    request: Request,
    db: AsyncSession = Depends(get_db),
    access_token: Annotated[str | None, Cookie()] = None
):
    
    try:
        # Cookie ichidan tokenni ajratib olamiz
        cookie = loads(access_token)
        query = select(UserToken).where(UserToken.token == cookie.get("token"))
        result = await db.execute(query)
        session = result.scalar_one_or_none()
    except Exception:
        session = None

    user_query = await db.execute(select(User).where(User.id == session.user_id))
    user = user_query.scalar_one_or_none()
    
    if not user:
        raise Exception("User not found")
        
    if not checkadmin(user=user,db=db):
        raise HTTPException(403,"Siz Admin emassiz")
    
    return templates.TemplateResponse(name="admin.html", request=request, context={
        "request": request,
        "status": "AUTHORIZED",
        "theme": "dark",
        "username": user.username,
        "background": user.background,
        "title": "Subject Hub admin panel"
    })

