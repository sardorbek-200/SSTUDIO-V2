from json import loads
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.models import UserToken, User

async def get_authenticated_user(access_token: Optional[str], db: AsyncSession):
    if access_token is None:
        return None

    try:
        session = loads(access_token)
    except Exception:
        return None

    token = session.get("token")
    if token is None:
        return None

    user_token_result = await db.execute(select(UserToken).where(UserToken.token == token))
    user_token = user_token_result.scalar_one_or_none()
    if user_token is None:
        return None

    user_result = await db.execute(select(User).where(User.id == user_token.user_id))
    return user_result.scalar_one_or_none()
