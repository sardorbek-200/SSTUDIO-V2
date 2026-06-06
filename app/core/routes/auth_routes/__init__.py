from fastapi import APIRouter, Request # Request ni import qilishni unutmang!
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from ...config import templates_path
from ..auth_routes.sign_in import auth as sign_in_router
from ..auth_routes.sign_up import auth as sign_up_router
from ..auth_routes.logout import router as logout_router
auth = APIRouter(prefix="/auth") # Barcha auth yo'llari /auth bilan boshlanadi
templates = Jinja2Templates(directory=templates_path+"/auth")
auth.include_router(sign_in_router) # sign-in routerini auth routeriga qo'shamiz
auth.include_router(sign_up_router) # sign-up routerini auth routeriga qo'shamiz
auth.include_router(logout_router) # logout routerini auth routeriga qo'shamiz
# Dekorator ichidagi ortiqcha narsalarni olib tashladik
@auth.get("/", response_class=HTMLResponse)
async def login_page(request: Request): # request: Request tipini belgilang
    return templates.TemplateResponse(
        request=request, 
        name="auth.html", 
        context={
            "request": request,
            "theme": "dark",
            "title": "Kirish sahifasi",
            "background": "/static/images/default_bg.png",
            "lang": "uz"
        }
    )