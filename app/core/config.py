import os
from dotenv import load_dotenv
load_dotenv("D:")

class Settings:
    PROJECT_NAME = os.getenv("PROJECT_NAME", "S-Studio")
    AI = os.getenv("AI")
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    DATABASE_URL = os.getenv("DATABASE_URL")

templates_path = "./app/templates"
TELEGRAM_BOT_USERNAME = os.getenv("TELEGRAM_BOT_USERNAME")
TG_TOKEN = os.getenv("TG_TOKEN")