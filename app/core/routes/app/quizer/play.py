from fastapi import APIRouter, Depends, Request, Cookie
from json import loads,dumps
from fastapi.responses import RedirectResponse, JSONResponse
from ....database import  get_db
from ....models import User, UserAllowedTest, UserToken, Tests, Questions, TestResult, UserOptions
from ....config import templates_path
from sqlalchemy import select
from fastapi.templating import Jinja2Templates
from typing import Annotated
from fastapi.exceptions import HTTPException
router = APIRouter()
templates = Jinja2Templates(templates_path)


@router.get("/test/{test_id}/play")
async def play_test(request:Request,test_id: int,  db=Depends(get_db), access_token: Annotated[str, Cookie()] = None):
    if access_token is None:
        return RedirectResponse(url="/auth/sign-in",status_code=302)
    session = loads(access_token)
    user_query = await db.execute(select(UserToken).where(UserToken.token == session.get("token")))
    user = user_query.scalar_one_or_none()
    if not user:
        return RedirectResponse(url="/auth/sign-in",status_code=302)
    user_query = await db.execute(select(User).where(User.id == user.user_id))
    user = user_query.scalar_one_or_none()
    # Check if the user is allowed to take the test
    

    # Fetch the test and its questions
    test = await db.execute(select(Tests).where(Tests.id == test_id))
    test = test.scalar_one_or_none()
    if not test:
        return {"error": "Test not found."}
    if not test.is_public:
        allowed_test = await db.execute(select(UserAllowedTest).where(UserAllowedTest.user_id == user.id, UserAllowedTest.test_id == test_id))
        allowed_test = allowed_test.scalar_one_or_none()
        if not allowed_test:
            return {"error": "You are not allowed to take this test."}
    response =  templates.TemplateResponse(name="quizer/play.html",request=request, context={ "test": test,"title":"Quizer - Test Ishlash","theme":"dark", "lang":"uz","background":user.background, "username":user.username, "status":"AUTHORIZED"})
    response.set_cookie(key="access_token",value=access_token,httponly=True)
    return response


@router.get("/test/{test_id}/questions")
async def get_test_questions(
    test_id: int, 
    db = Depends(get_db), 
    access_token : Annotated[str, Cookie()] = None
):
    if access_token is None:
        return RedirectResponse(url="/auth/sign-in",status_code=302)
    session = loads(access_token)
    user_query = await db.execute(select(UserToken).where(UserToken.token == session.get("token")))
    user = user_query.scalar_one_or_none()
    if not user:
        return RedirectResponse(url="/auth/sign-in",status_code=302)
    user_query = await db.execute(select(User).where(User.id == user.user_id))
    user = user_query.scalar_one_or_none()
    # Check if the user is allowed to take the test
    

    # 1. TestResult jadvalini asinxron SELECT orqali tekshiramiz
    result_stmt = select(UserOptions).filter(
        UserOptions.test_id == test_id,
        UserOptions.user_id == user.id,
        UserOptions.end == True
    )
    result_query = await db.execute(result_stmt)
    existing_result = result_query.scalars().first()

    # Agar foydalanuvchi bu testni tugatgan bo'lsa, savollarni bermaymiz
    if existing_result:
        return {"status": "already_finished", "questions": []}

    # 2. Test mavjudligini asinxron tekshiramiz
    test_stmt = select(Tests).filter(Tests.id == test_id)
    test_query = await db.execute(test_stmt)
    test = test_query.scalars().first()
    
    if not test:
        raise HTTPException(status_code=404, detail="Test topilmadi")

    # 3. Savollarni asinxron yuklaymiz
    question_stmt = select(Questions).filter(Questions.test_id == test_id)
    question_query = await db.execute(question_stmt)
    questions = question_query.scalars().all()
    
    # Frontend uchun ma'lumotlarni tayyorlaymiz
    questions_data = []
    for q in questions:
        questions_data.append({
            "id": q.id,
            "text": q.question_text,
            "options": [q.option_a, q.option_b, q.option_c, q.option_d]
        })

    return {"status": "success", "questions": questions_data}


# 2. Javobni saqlash (Har bir bosganda)
@router.post("/test/{test_id}/option")
async def save_option(request: Request, test_id: int, db=Depends(get_db), access_token: Annotated[str | None, Cookie()] = None):
    if not access_token:
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    
    cookie = loads(access_token)
    query = select(UserToken).where(UserToken.token == cookie.get("token"))
    result = await db.execute(query)
    session = result.scalar_one_or_none()
    # UserOptions ni topamiz yoki yaratamiz
    opt = await db.execute(select(UserOptions).where(UserOptions.test_id == test_id, UserOptions.user_id == session.user_id))
    user_opt = opt.scalar_one_or_none()
    
    if not user_opt:
        user_opt = UserOptions(user_id=session.user_id, test_id=test_id, options=dumps([]))
        db.add(user_opt)
    data = await request.json()
    # Javobni saqlash logikasi
    # 1. Bazadagi mavjud javoblarni yuklab olamiz
    current_options = loads(user_opt.options)
    # 2. Yangi kelgan ma'lumot (bu dict)
    new_answer = {
        "question_id": data["question_id"], 
        "options": data["option_index"]
    }
    
    # 3. Logika: Agar shu savolga avval javob berilgan bo'lsa, uni yangilaymiz, 
    # agar bo'lmasa, yangi javob sifatida qo'shamiz
    found = False
    for i, item in enumerate(current_options):
        if item["question_id"] == new_answer["question_id"]:
            current_options[i] = new_answer  # Eski javobni yangilash
            found = True
            break
            
    if not found:
        current_options.append(new_answer)  # Yangi savol bo'lsa ro'yxatga qo'shish
    
    # 4. Yangilangan ro'yxatni bazaga qaytarib saqlaymiz
    user_opt.options = dumps(current_options)
    await db.commit()
    return {"status": "ok"}

# 3. Testni yakunlash (Natijani hisoblash)
@router.post("/test/{test_id}/finish")
async def finish_test(test_id: int, db=Depends(get_db),access_token : Annotated[str, Cookie()] = None):
    if not access_token:
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    
    cookie = loads(access_token)
    query = select(UserToken).where(UserToken.token == cookie.get("token"))
    result = await db.execute(query)
    session = result.scalar_one_or_none()
    # UserOptions ni topamiz yoki yaratamiz
    opt = await db.execute(select(UserOptions).where(UserOptions.test_id == test_id, UserOptions.user_id == session.user_id))
    user_opt = opt.scalar_one_or_none()
    
    if not user_opt:
        user_opt = UserOptions(user_id=session.user_id, test_id=test_id, options=dumps([]))
        db.add(user_opt)
    user_opt.end= True
    await db.commit()
    
    return {"status": "finished", "result": 85}