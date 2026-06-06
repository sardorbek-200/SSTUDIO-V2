from fastapi import APIRouter, Depends, Request, Cookie
from fastapi.responses import JSONResponse  # To'g'ri nomlanishi JSONResponse
from ....models import User, Tests, UserAllowedTest, UserToken
from ....database import get_db
from typing import Annotated
from sqlalchemy import select
from json import loads

router = APIRouter(prefix="/api", tags=["quizer api"])

# --- 1. RASMIY / OMMAVIY TESTLAR ---
@router.get("/public-tests")
async def get_public_tests(db = Depends(get_db)):
    query = select(Tests).where(Tests.is_public == True, Tests.status == "active")

    result = await db.execute(query)
    tests = result.scalars().all()

    # 2. Obyektlarni dict formatiga xavfsiz o'tkazamiz
    formatted_tests = []
    for test in tests:
        # Obyekt nusxasini olamiz, asl bazadagi holatiga tegmaymiz
        test_data = test.__dict__.copy() 
        test_data.pop('_sa_instance_state', None)  # Ichki SQLAlchemy holatini olib tashlaymiz
        formatted_tests.append(test_data)

    return {"tests": formatted_tests}
# --- 2. RO'YHATDAN O'TILGAN (RUXSAT BERILGAN) TESTLAR ---
@router.get("/user-allowed-tests")
async def get_user_allowed_tests(request: Request, db = Depends(get_db), access_token: Annotated[str | None, Cookie()] = None):
    if not access_token:
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    
    cookie = loads(access_token)
    query = select(UserToken).where(UserToken.token == cookie.get("token"))
    result = await db.execute(query)
    session = result.scalar_one_or_none()
    
    if not session or session.ip_address != request.client.host:
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
        
    user_query = await db.execute(select(User).where(User.id == session.user_id))
    user = user_query.scalar_one_or_none()
    if not user:
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
        
    allowed_tests_query = await db.execute(select(UserAllowedTest).where(UserAllowedTest.user_id == user.id))
    allowed_tests = allowed_tests_query.scalars().all()
    test_ids = [allowed_test.test_id for allowed_test in allowed_tests]
    
    if not test_ids:
        return {"allowed_tests": []}
        
    tests_query = await db.execute(select(Tests).where(Tests.id.in_(test_ids)))
    tests = tests_query.scalars().all()
    formatted_tests = []
    for test in tests:
        # Obyekt nusxasini olamiz, asl bazadagi holatiga tegmaymiz
        test_data = test.__dict__.copy() 
        test_data.pop('_sa_instance_state', None)  # Ichki SQLAlchemy holatini olib tashlaymiz
        formatted_tests.append(test_data)
    return {"allowed_tests": formatted_tests}
# --- 3. TESTGA RUXSAT QO'SHISH (ADD) ---
@router.get("/test/{test_id}/add")
async def add_test_to_allowed(test_id: int, request: Request, db = Depends(get_db), access_token: Annotated[str | None, Cookie()] = None): # Funksiya nomi o'zgardi
    if not access_token:
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    
    cookie = loads(access_token)
    query = select(UserToken).where(UserToken.token == cookie.get("token"))
    result = await db.execute(query)
    session = result.scalar_one_or_none()
    
    if not session or session.ip_address != request.client.host:
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
        
    user_query = await db.execute(select(User).where(User.id == session.user_id))
    user = user_query.scalar_one_or_none()
    if not user:
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
        
    test_query = await db.execute(select(Tests).where(Tests.id == test_id))
    test = test_query.scalar_one_or_none()
    if not test:
        return JSONResponse({"error": "Test not found"}, status_code=404)
        
    # Dublikat tekshiruvi (bitta testni ko'p marta qo'shib yubormaslik uchun)
    check_query = await db.execute(select(UserAllowedTest).where(UserAllowedTest.user_id == user.id, UserAllowedTest.test_id == test.id))
    already_exists = check_query.scalar_one_or_none()
    if already_exists:
        return {"message": "Already added"}

    new_test = UserAllowedTest(user_id=user.id, test_id=test.id)
    db.add(new_test)    
    await db.commit()
    return {"message": "OK"}

# --- 4. TEST SAVOLLARINI OLISH (DATA) ---
@router.get("/test/{test_id}/data")
async def get_test_questions_data(test_id: int, request: Request, db = Depends(get_db), access_token: Annotated[str | None, Cookie()] = None): # Funksiya nomi o'zgardi
    if not access_token:
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    
    cookie = loads(access_token)
    query = select(UserToken).where(UserToken.token == cookie.get("token"))
    result = await db.execute(query)
    session = result.scalar_one_or_none()
    
    if not session or session.ip_address != request.client.host:
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
        
    user_query = await db.execute(select(User).where(User.id == session.user_id))
    user = user_query.scalar_one_or_none()
    if not user:
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
        
    test_query = await db.execute(select(Tests).where(Tests.id == test_id))
    test = test_query.scalar_one_or_none()
    if not test:
        return JSONResponse({"error": "Test not found"}, status_code=404)
        
    return {"test_data": test.data}

# --- 5. MENING MAXFIY/YARATGAN TESTLARIM ---
@router.get("/my-tests")
async def get_my_tests(request: Request, db = Depends(get_db), access_token: Annotated[str | None, Cookie()] = None):
    if not access_token:
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    
    cookie = loads(access_token)
    query = select(UserToken).where(UserToken.token == cookie.get("token"))
    result = await db.execute(query)
    session = result.scalar_one_or_none()
    
    if not session or session.ip_address != request.client.host:
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
        
    user_query = await db.execute(select(User).where(User.id == session.user_id))
    user = user_query.scalar_one_or_none()
    if not user:
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
        
    allowed_tests_query = await db.execute(select(Tests).where(Tests.user_id == user.id))
    allowed_tests = allowed_tests_query.scalars().all()
    formatted_tests = []
    for test in allowed_tests:
        # Obyekt nusxasini olamiz, asl bazadagi holatiga tegmaymiz
        test_data = test.__dict__.copy() 
        test_data.pop('_sa_instance_state', None)  # Ichki SQLAlchemy holatini olib tashlaymiz
        formatted_tests.append(test_data)
    return {"allowed_tests": formatted_tests}
@router.get("/scoin")
async def get_user_scoin(request: Request, db = Depends(get_db), access_token: Annotated[str | None, Cookie()] = None):
    if not access_token:
        return JSONResponse({"error": "Unauthorized"}, status_code=401)

    cookie = loads(access_token)
    query = select(UserToken).where(UserToken.token == cookie.get("token"))
    result = await db.execute(query)
    session = result.scalar_one_or_none()

    if not session or session.ip_address != request.client.host:
        return JSONResponse({"error": "Unauthorized"}, status_code=401)

    user_query = await db.execute(select(User).where(User.id == session.user_id))
    user = user_query.scalar_one_or_none()
    if not user:
        return JSONResponse({"error": "Unauthorized"}, status_code=401)

    return {"scoin": user.scoin}
    