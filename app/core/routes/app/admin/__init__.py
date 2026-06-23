from typing import Annotated
from json import loads
from fastapi import APIRouter, Depends, Request, Cookie, HTTPException, Body
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

# Ichki modullardan importlar
from ....database import get_db
from ....config import templates_path
from .check import checkadmin, get_admin_user
from app.core.models import User, UserToken, Admin, Tests, Questions
from .statistik import router as IRouter
from .controlsshop import router as IRouter1

# Jinja2 sozlamasi
template = Jinja2Templates(directory=templates_path)

router = APIRouter(prefix="/admin", tags=["admin"])
router.include_router(IRouter)
router.include_router(IRouter1)

# ==========================================================================
# 🔍 UTILITY (HELPER) FUNKSIYALAR
# ==========================================================================

async def get_current_user(db: AsyncSession, access_token: str):
    """Cookie orqali joriy foydalanuvchi seansini aniqlash"""
    if not access_token:
        return None
    try:
        cookie = loads(access_token)
        token_str = cookie.get("token")
    except Exception:
        return None
    
    query = select(UserToken).where(UserToken.token == token_str)
    result = await db.execute(query)
    return result.scalar_one_or_none()


# ==========================================================================
# 📊 1. ADMIN PANEL ASOSIY SAHIFASI
# ==========================================================================

@router.get("/", response_class=HTMLResponse)
async def admin_dashboard(
    request: Request,
    db: AsyncSession = Depends(get_db),
    access_token: Annotated[str | None, Cookie()] = None
):
    current_user = await get_admin_user(db, access_token)
    if not current_user:
        return RedirectResponse(url="/auth/sign-in", status_code=302)

    is_admin = await checkadmin(db, current_user)
    if not is_admin:
        raise HTTPException(status_code=403, detail="Siz admin emassiz")

    response = template.TemplateResponse(
        name="admin/admin.html",
        request=request,
        context={
            "request": request,
            "status": "AUTHORIZED",
            "user": current_user.username,
            "username": current_user.username,
            "title": "Admin Panel",
            "background": current_user.background,
            "admin": is_admin
        }
    )
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response


# ==========================================================================
# 🛡️ 2. ADMINLAR JADVALINI BOSHQARISH (YANGI ARXITEKTURA)
# ==========================================================================

@router.get("/admins", response_class=HTMLResponse)
async def manage_admins_page(
    request: Request,
    db: AsyncSession = Depends(get_db),
    access_token: Annotated[str | None, Cookie()] = None,
):
    current_user = await get_admin_user(db, access_token)
    if not current_user:
        return RedirectResponse(url="/auth/sign-in", status_code=302)

    is_admin = await checkadmin(db, current_user)
    if not is_admin:
        raise HTTPException(status_code=403, detail="Siz admin emassiz")

    # Tizimdagi adminlarni tegishli User ma'lumotlari bilan yuklab olish
    admins_query = await db.execute(
        select(Admin).options(selectinload(Admin.user)).order_by(Admin.id.desc())
    )
    admins_list = admins_query.scalars().all()

    # Dropdown (select) uchun hali admin bo'lmagan foydalanuvchilar ro'yxati
    admin_user_ids = [admin.user_id for admin in admins_list]
    if admin_user_ids:
        non_admins_query = await db.execute(
            select(User).where(User.id.notin_(admin_user_ids)).order_by(User.id.desc())
        )
    else:
        non_admins_query = await db.execute(select(User).order_by(User.id.desc()))
        
    non_admins = non_admins_query.scalars().all()

    response = template.TemplateResponse(
        name="admin/admins.html",
        request=request,
        context={
            "request": request,
            "status": "AUTHORIZED",
            "username": current_user.username,
            "title": "Adminlar Boshqaruvi",
            "background": current_user.background,
            "admin": is_admin,
            "admins": admins_list,
            "non_admins": non_admins
        }
    )
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response


@router.post("/add_admin")
async def add_admin_role(
    data: dict = Body(...),
    db: AsyncSession = Depends(get_db),
    access_token: Annotated[str | None, Cookie()] = None,
):
    current_user = await get_admin_user(db, access_token)
    if not current_user or not await checkadmin(db, current_user):
        return JSONResponse(status_code=403, content={"detail": "Ruxsat yo'q"})

    username = data.get("username")
    if not username:
        return JSONResponse(status_code=400, content={"detail": "Foydalanuvchi nomi kiritilmadi"})

    target_query = await db.execute(select(User).where(User.username == username))
    target_user = target_query.scalar_one_or_none()
    if not target_user:
        return JSONResponse(status_code=404, content={"detail": "Foydalanuvchi topilmadi"})

    existing_admin_query = await db.execute(select(Admin).where(Admin.user_id == target_user.id))
    if existing_admin_query.scalar_one_or_none():
         return JSONResponse(status_code=400, content={"detail": "Bu foydalanuvchi allaqachon admin!"})

    new_admin = Admin(user_id=target_user.id)
    db.add(new_admin)
    await db.commit()
    return JSONResponse(status_code=200, content={"message": f"{username} muvaffaqiyatli admin bo'ldi!"})


@router.post("/remove_admin/{admin_id}")
async def remove_admin_role(
    admin_id: int,
    db: AsyncSession = Depends(get_db),
    access_token: Annotated[str | None, Cookie()] = None,
):
    current_user = await get_admin_user(db, access_token)
    if not current_user or not await checkadmin(db, current_user):
        return JSONResponse(status_code=403, content={"detail": "Ruxsat yo'q"})

    target_query = await db.execute(select(Admin).where(Admin.id == admin_id))
    target_admin = target_query.scalar_one_or_none()
    if not target_admin:
        return JSONResponse(status_code=404, content={"detail": "Admin topilmadi"})

    if target_admin.user_id == current_user.id:
        return JSONResponse(status_code=400, content={"detail": "O'zingizni adminlikdan ola olmaysiz!"})

    await db.delete(target_admin)
    await db.commit()
    return JSONResponse(status_code=200, content={"message": "Adminlik huquqi o'chirildi"})


# ==========================================================================
# 👥 3. FOYDALANUVCHILARNI BOSHQARISH (CRUD)
# ==========================================================================

@router.get("/users", response_class=HTMLResponse)
async def admin_users(
    request: Request,
    db: AsyncSession = Depends(get_db),
    access_token: Annotated[str | None, Cookie()] = None,
):
    current_user = await get_admin_user(db, access_token)
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


@router.post("/edit_user/{id}")
async def admin_edit_user(
    id: int,
    data: dict = Body(...),
    db: AsyncSession = Depends(get_db),
    access_token: Annotated[str | None, Cookie()] = None,
):
    current_user = await get_admin_user(db, access_token)
    if not current_user or not await checkadmin(db, current_user):
        return JSONResponse(status_code=403, content={"detail": "Ruxsat berilmagan"})

    target_query = await db.execute(select(User).where(User.id == id))
    target_user = target_query.scalar_one_or_none()
    if not target_user:
        return JSONResponse(status_code=404, content={"detail": "Foydalanuvchi topilmadi"})

    username = data.get("username")
    xp = data.get("xp")
    scoin = data.get("scoin")

    if username and username.strip() != "":
        username = username.strip()
        if username != target_user.username:
            existing_query = await db.execute(select(User).where(User.username == username))
            if existing_query.scalar_one_or_none():
                return JSONResponse(status_code=400, content={"detail": "Bu foydalanuvchi nomi band"})
            target_user.username = username

    if xp is not None and xp != "":
        try:
            target_user.xp = int(xp)
        except ValueError:
            return JSONResponse(status_code=400, content={"detail": "XP butun son bo'lishi kerak"})

    if scoin is not None and scoin != "":
        try:
            target_user.scoin = int(scoin)
        except ValueError:
            return JSONResponse(status_code=400, content={"detail": "sCoin butun son bo'lishi kerak"})

    await db.commit()
    return JSONResponse(status_code=200, content={"message": "Muvaffaqiyatli yangilandi"})


@router.post("/delete_user/{id}")
async def admin_delete_user(
    id: int,
    db: AsyncSession = Depends(get_db),
    access_token: Annotated[str | None, Cookie()] = None,
):
    current_user = await get_admin_user(db, access_token)
    if not current_user or not await checkadmin(db, current_user):
        return JSONResponse(status_code=403, content={"detail": "Ruxsat berilmagan"})

    target_query = await db.execute(select(User).where(User.id == id))
    target_user = target_query.scalar_one_or_none()
    if not target_user:
        return JSONResponse(status_code=404, content={"detail": "Foydalanuvchi topilmadi"})

    await db.delete(target_user)
    await db.commit()
    return JSONResponse(status_code=200, content={"message": "Foydalanuvchi o'chirildi"})


# ==========================================================================
# 📝 4. TEST VA SAVOLLARNI TAHRIRLASH TIZIMI
# ==========================================================================

@router.get("/edit", response_class=HTMLResponse)
async def edit_main_page(
    request: Request, 
    db: AsyncSession = Depends(get_db), 
    access_token: Annotated[str | None, Cookie()] = None
):
    session = await get_current_user(db, access_token)
    if not session or session.ip_address != request.client.host:
        return RedirectResponse(url="/auth/login")
    
    user_query = await db.execute(select(User).where(User.id == session.user_id))
    user = user_query.scalar_one_or_none()
    if not user or not await checkadmin(db, user):
        raise HTTPException(status_code=403, detail="Siz Admin emassiz")
        
    tests_query = await db.execute(select(Tests))
    all_tests = tests_query.scalars().all()
 
    return template.TemplateResponse(
        name="admin/edit.html", 
        request=request, 
        context={
            "request": request,
            "username": user.username,
            "title": "Testlarni Tahrirlash",
            "scoin": user.scoin,
            "status": "AUTHORIZED",
            "background": user.background,
            "tests": all_tests
        }
    )


@router.get("/api/get-test/{test_id}")
async def api_get_test_data(
    test_id: int,
    db: AsyncSession = Depends(get_db),
    access_token: Annotated[str | None, Cookie()] = None,
):
    current_user = await get_admin_user(db, access_token)
    if not current_user or not await checkadmin(db, current_user):
        return JSONResponse({"status": "error", "message": "Ruxsat yo'q"}, status_code=403)
        
    test_query = await db.execute(select(Tests).where(Tests.id == test_id, Tests.status == "active"))
    test = test_query.scalar_one_or_none()
    if not test:
        return JSONResponse({"status": "error", "message": "Test topilmadi"}, status_code=404)

    questions_query = await db.execute(select(Questions).where(Questions.test_id == test_id))
    questions = questions_query.scalars().all()

    questions_data = [{
        "id": q.id,
        "question_text": q.question_text,
        "option_a": q.option_a,
        "option_b": q.option_b,
        "option_c": q.option_c,
        "option_d": q.option_d,
        "correct_option": q.correct_answer
    } for q in questions]

    return {
        "status": "success",
        "test": {
            "id": test.id,
            "title": test.title,
            "description": test.description,
            "status": test.status
        },
        "questions": questions_data
    }


@router.post("/edit/question/{question_id}/update")
async def update_question_data(
    question_id: int,
    data: dict,
    db: AsyncSession = Depends(get_db),
    access_token: Annotated[str | None, Cookie()] = None,
):
    current_user = await get_admin_user(db, access_token)
    if not current_user or not await checkadmin(db, current_user):
        return JSONResponse({"status": "error", "message": "Ruxsat yo'q"}, status_code=403)

    try:
        stmt = update(Questions).where(Questions.id == question_id).values(
            question_text=data.get("question_text"),
            option_a=data.get("option_a"),
            option_b=data.get("option_b"),
            option_c=data.get("option_c"),
            option_d=data.get("option_d"),
            correct_answer=data.get("correct_option")
        )
        await db.execute(stmt)
        await db.commit()
        return {"status": "success", "message": "Savol muvaffaqiyatli yangilandi!"}
    except Exception as e:
        await db.rollback()
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)


@router.post("/edit/{test_id}/update-info")
async def update_test_info(
    test_id: int,
    data: dict,
    db: AsyncSession = Depends(get_db),
    access_token: Annotated[str | None, Cookie()] = None,
):
    current_user = await get_admin_user(db, access_token)
    if not current_user or not await checkadmin(db, current_user):
        return JSONResponse({"status": "error", "message": "Ruxsat yo'q"}, status_code=403)

    try:
        stmt = update(Tests).where(Tests.id == test_id).values(
            title=data.get("title"),
            description=data.get("description"),
            status=data.get("status")
        )
        await db.execute(stmt)
        await db.commit()
        return {"status": "success", "message": "Test sozlamalari saqlandi!"}
    except Exception as e:
        await db.rollback()
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)


@router.post("/edit/{test_id}/force-stop")
async def force_stop_test(
    test_id: int,
    db: AsyncSession = Depends(get_db),
    access_token: Annotated[str | None, Cookie()] = None,
):
    current_user = await get_admin_user(db, access_token)
    if not current_user or not await checkadmin(db, current_user):
        return JSONResponse({"status": "error", "message": "Ruxsat yo'q"}, status_code=403)

    try:
        stmt = update(Tests).where(Tests.id == test_id).values(status="stopped")
        await db.execute(stmt)
        await db.commit()
        return {"status": "success", "message": f"Test #{test_id} majburiy to'xtatildi!"}
    except Exception as e:
        await db.rollback()
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)