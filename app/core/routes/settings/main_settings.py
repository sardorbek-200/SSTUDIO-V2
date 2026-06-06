from fastapi import APIRouter, Request, Depends, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from json import loads
from typing import Annotated
from ...database import get_db
from ...models import User, UserToken
from ...config import templates_path

router = APIRouter()
templates = Jinja2Templates(directory=templates_path)


@router.get("/settings", response_class=HTMLResponse)
async def settings_page(
    request: Request,
    db: AsyncSession = Depends(get_db),
    access_token: Annotated[str | None, Cookie()] = None
):
    """Settings sahifasini ko'rsatish"""
    if not access_token:
        return RedirectResponse(url="/auth", status_code=302)
    
    try:
        cookie = loads(access_token)
        token = cookie.get("token")
        
        # Token orqali userga kirish
        query = select(UserToken).where(UserToken.token == token)
        result = await db.execute(query)
        session = result.scalar_one_or_none()
        
        if not session:
            return RedirectResponse(url="/auth", status_code=302)
        
        # Userga kirish
        user_query = await db.execute(select(User).where(User.id == session.user_id))
        user = user_query.scalar_one_or_none()
        
        if not user:
            return RedirectResponse(url="/auth", status_code=302)
        
        # Settings sahifasini ko'rsatish
        return templates.TemplateResponse(
            request=request,
            name="settings.html",
            context={
                "request": request,
                "status": "AUTHORIZED",
                "username": user.username,
                "theme": user.theme,
                "lang": user.language,
                "title": "Sozlamalar",
                "background": user.background
            }
        )
    except Exception as e:
        print(f"Error in settings_page: {str(e)}")
        return RedirectResponse(url="/auth", status_code=302)
