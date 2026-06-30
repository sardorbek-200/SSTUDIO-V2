from fastapi.responses import RedirectResponse
from fastapi import APIRouter

router = APIRouter()

@router.get("/logout")
async def logout():
    # 1. Bosh sahifaga yo'naltirish ob'ektini olamiz
    response = RedirectResponse(url="/", status_code=303)
    
    # 2. Brauzerdagi cookieni o'chirib tashlaymiz
    response.delete_cookie(key="access_token",domain=".sstudio.uz")
    
    return response