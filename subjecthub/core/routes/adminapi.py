from fastapi import APIRouter, Depends, HTTPException, Cookie, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Annotated
import json # 👈 json ni import qilamiz
from json import loads
from ..models import User, UserToken, SubjectHubQuestion
from ..database import get_db
from .check import checkadmin
import httpx
from ...config import Settings
API_KEY = Settings.AI
# Agar 3.5 Flash ishlatmoqchi bo'lsang:
# Gemini 3 Flash o'rniga:
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite:generateContent?key={API_KEY}"
router = APIRouter(prefix="/api/admin/questions", tags=["Admin Questions"])

# ... get_current_admin funksiyasi o'zgarishsiz ...

async def get_current_admin(
    access_token: Annotated[str | None, Cookie()] = None,
    db: AsyncSession = Depends(get_db)
):
    if not access_token:
        raise HTTPException(status_code=401, detail="Token topilmadi")
    try:
        cookie = loads(access_token)
        query = select(UserToken).where(UserToken.token == cookie.get("token"))
        result = await db.execute(query)
        session = result.scalar_one_or_none()
        
        if not session:
            raise HTTPException(status_code=401, detail="Sessiya yaroqsiz")
            
        user_query = await db.execute(select(User).where(User.id == session.user_id))
        user = user_query.scalar_one_or_none()
        
        if not user or not checkadmin(user=user, db=db):
            raise HTTPException(status_code=403, detail="Siz Admin emassiz!")
            
        return user
    except Exception:
        raise HTTPException(status_code=401, detail="Avtorizatsiya xatosi")

@router.post("/generate-ai")
async def generate_ai(request: Request, db: AsyncSession = Depends(get_db)):
    data = await request.json()
    topic = data.get("topic")
    count = data.get("count")

    prompt_text = (
        f"Menga {topic} fanidan {count} ta test savolini JSON formatida tuzib ber. "
        "Har bir savol quyidagi kalitlarga ega bo'lishi kerak: text, options (4 ta variantlik list), correct_answer, subject. "
        "Faqat toza JSON ro'yxatini qaytar, qo'shimcha hech narsa yozma."
    )
    prompt = {
        "contents": [{
            "parts": [{"text": prompt_text}]
        }]
    }
    async with httpx.AsyncClient(timeout=httpx.Timeout(60.0, connect=10.0)) as client:
        response = await client.post(URL, json=prompt)
        result = response.json() 
    
    # XATOLIKNI TEKSHIRAMIZ
    if 'candidates' not in result:
        print("API javobi xatoli:", result) # Konsolda nima kelganini ko'ramiz
        raise HTTPException(status_code=500, detail=f"API xatosi: {result.get('error', 'Noma\'lum xatolik')}")

    # Davom etamiz...
    text = result['candidates'][0]['content']['parts'][0]['text']
    clean_text = text.replace("```json", "").replace("```", "").strip()
    
    try:
        questions = json.loads(clean_text)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="AI noto'g'ri formatda ma'lumot qaytardi")

    for q in questions:
        new_q = SubjectHubQuestion(
            text=q['text'],
            options=json.dumps(q['options']),
            correct_answer=q['correct_answer'],
            subject=q['subject']
        )
        db.add(new_q)
    
    await db.commit()
    return {"message": f"{len(questions)} ta savol qo'shildi!"}




# 1. READ (Bazadagi stringni listga o'giramiz)
@router.get("/")
async def get_questions(db: AsyncSession = Depends(get_db), admin: User = Depends(get_current_admin)):
    result = await db.execute(select(SubjectHubQuestion))
    questions = result.scalars().all()
    
    return [
        {
            "id": q.id,
            "text": q.text,
            "options": json.loads(q.options), # 👈 String ni listga o'giramiz
            "correct_answer": q.correct_answer,
            "subject": q.subject
        } for q in questions
    ]

# 2. CREATE (Frontend'dan kelgan listni stringga o'giramiz)
@router.post("/")
async def create_question(request: Request, db: AsyncSession = Depends(get_db), admin: User = Depends(get_current_admin)):
    data = await request.json()
    
    new_q = SubjectHubQuestion(
        text=data.get("text"),
        options=json.dumps(data.get("options")), # 👈 List ni stringga o'giramiz
        correct_answer=data.get("correct_answer"),
        subject=data.get("subject")
    )
    
    db.add(new_q)
    await db.commit()
    await db.refresh(new_q)
    return {"message": "Savol qo'shildi"}

# 3. UPDATE (Edit)
@router.put("/{question_id}")
async def update_question(question_id: int, request: Request, db: AsyncSession = Depends(get_db), admin: User = Depends(get_current_admin)):
    query = await db.execute(select(SubjectHubQuestion).where(SubjectHubQuestion.id == question_id))
    question = query.scalar_one_or_none()
    if not question:
        raise HTTPException(status_code=404, detail="Savol topilmadi")
    
    data = await request.json()
    
    question.text = data.get("text", question.text)
    # 👈 Tahrirlashda ham listni stringga o'giramiz
    if "options" in data:
        question.options = json.dumps(data.get("options"))
    question.correct_answer = data.get("correct_answer", question.correct_answer)
    question.subject = data.get("subject", question.subject)
    
    await db.commit()
    return {"message": "Savol tahrirlandi"}

# 4. DELETE
@router.delete("/{question_id}")
async def delete_question(
    question_id: int,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    query = await db.execute(select(SubjectHubQuestion).where(SubjectHubQuestion.id == question_id))
    question = query.scalar_one_or_none()
    
    if not question:
        raise HTTPException(status_code=404, detail="Savol topilmadi")
    
    await db.delete(question)
    await db.commit()
    return {"message": "Savol o'chirildi"}