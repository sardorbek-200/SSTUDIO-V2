from fastapi import APIRouter,Depends,Request, Cookie
from fastapi.templating import Jinja2Templates
from ...config import templates_path
from ...models import UserToken, User, Status
from json import loads
from ...database import get_db
from sqlalchemy import select
from fastapi.responses import RedirectResponse
from typing import Annotated
from .list import router as list_router


template = Jinja2Templates(directory=templates_path)

router = APIRouter(prefix="/users")
router.include_router(list_router)

@router.get("/{id}")
async def quizer(request: Request, db = Depends(get_db), access_token: Annotated[str | None, Cookie()] = None):
    if not access_token:
        return RedirectResponse(url="/auth/login")
        
    try:
        cookie = loads(access_token)
        token_str = cookie.get("token")
    except Exception:
        return RedirectResponse(url="/auth/login")
        
    query = select(UserToken).where(UserToken.token == token_str)
    result = await db.execute(query)
    session = result.scalar_one_or_none()
    
    if not session:
        return RedirectResponse(url="/auth/login")
        
    client_ip = request.client.host
    if session.ip_address != client_ip:
        return RedirectResponse(url="/auth/login")
        
    user_query = await db.execute(select(User).where(User.id == session.user_id))
    user = user_query.scalar_one_or_none()
    
    if not user:
        raise Exception("User not found")
    
    status_query = await db.execute(select(Status).where(User.id == Status.user_id))
    status = status_query.scalar_one_or_none()

    return template.TemplateResponse(
        request=request,
        name="user_for_iframe.html  ",
        context={
            "request":request,
            "user":user,
            "status":status
        }
    )

