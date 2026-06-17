from sqlalchemy import select
from ....models import Admin
async def checkadmin( db, user):
    admin_query = await db.execute(select(Admin).where(user.id==Admin.user_id))
    admin = admin_query.scalar_one_or_none()
    return True if admin else False