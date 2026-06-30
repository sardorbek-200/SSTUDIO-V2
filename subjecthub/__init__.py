from fastapi import FastAPI
from .config import Settings
from .core.routes import router as api_router


app = FastAPI(
    title=Settings.PROJECT_NAME,
    description="S-Studio: Yuqori tezlikdagi va xavfsiz Subject Hub backend tizimi",
    version="2.1.1",
)

# Barcha birlashtirilgan routerlarni bitta buyruq bilan FastAPI'ga ulaymiz
app.include_router(api_router)
