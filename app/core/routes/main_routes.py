from fastapi.responses import HTMLResponse
from ..models import User,UserToken
from sqlalchemy import select, func
from fastapi import APIRouter, Request, Depends, Cookie
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from ..config import templates_path
from ..database import get_db
from json import loads, dumps
from ..models import clean_old_test_results
templates = Jinja2Templates(directory=templates_path)
router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def home_page(request: Request,db:AsyncSession=Depends(get_db),access_token: Annotated[str | None, Cookie()] = None):
    total_users_query = await db.execute(select(func.count(User.id)))
    total_users = total_users_query.scalar()
    top_users_query = await db.execute(
        select(User).order_by(User.xp.desc()).limit(3)
    )
    top_users = top_users_query.scalars().all()
    if len(top_users)<3:
        top_users = [[],[],[]]
    if not access_token:
        return templates.TemplateResponse(name="index.html", request=request, context={
            "request": request,
            "status": "UNAUTHORIZED",
            "theme": "dark",
            "total_users": total_users,
            "top_users": top_users,
            "title": "Bosh sahifa",
            # "username": "Sstudio --",
            "background": "/static/images/default_bg.png",
            "lang":"uz" 
        })
    cookie = loads(access_token)
    query = select(UserToken).where(UserToken.token == cookie.get("token"))
    result = await db.execute(query)
    session = result.scalar_one_or_none()
    if not session:
        return templates.TemplateResponse(name="index.html", request=request, context={
            "request": request,
            "status": "UNAUTHORIZED",
            "theme": "dark",
            "total_users": total_users,
            "top_users": top_users,
            "title": "Bosh sahifa",
            # "username": "Sstudio --",
            "background": "/static/images/default_bg.png",
            "lang":"uz" 
        })
    user_query = await db.execute(select(User).where(User.id == session.user_id))
    user = user_query.scalar_one_or_none()
    client_ip = request.client.host
    if session.ip_address != client_ip:
        return templates.TemplateResponse(name="index.html", request=request, context={
            "request": request,
            "status": "UNAUTHORIZED",
            "theme": "dark",
            "total_users": total_users,
            "top_users": top_users,
            "title": "Bosh sahifa",
            "background": "/static/images/default_bg.png",
            "lang":"uz" 
        })
    if not user:
        raise Exception("User not found")
    response = templates.TemplateResponse(name="index.html", request=request, context={
        "request": request,
        "status": "AUTHORIZED",
        "theme": "dark",
        "username": user.username,
        "total_users": total_users,
        "top_users": top_users,
        "background": user.background ,
        "title": "Bosh sahifa"
    })
    response.set_cookie(key="access_token", value=dumps({"token": session.token}), httponly=True)
    return response

@router.get("/clear-old-results")
async def clear_old_results(db:AsyncSession=Depends(get_db)):
    return {"message": await clean_old_test_results(db)}