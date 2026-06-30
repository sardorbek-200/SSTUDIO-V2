from json import loads
from sqlalchemy import select
from ..models import Admin, UserToken, User

async def checkadmin(db, user):
    admin_query = await db.execute(select(Admin).where(user.id == Admin.user_id))
    admin = admin_query.scalar_one_or_none()
    return bool(admin)

async def get_admin_user(db, access_token):
    if not access_token:
        return None

    try:
        session = loads(access_token)
        token = session.get("token")
    except Exception:
        return None

    if not token:
        return None

    token_query = await db.execute(select(UserToken).where(UserToken.token == token))
    user_token = token_query.scalar_one_or_none()
    if not user_token:
        return None

    user_query = await db.execute(select(User).where(User.id == user_token.user_id))
    return user_query.scalar_one_or_none()