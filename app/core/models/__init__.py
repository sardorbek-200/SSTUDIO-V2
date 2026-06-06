from sqlalchemy import Column, Float, Integer, String, Boolean, DateTime, Text, ForeignKey, CHAR, desc
from sqlalchemy.sql import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta, timezone
from ..database import Base  # database.py faylidagi Base obyektini import qilasiz

# ==========================================
# 1. USER MODEL
# ==========================================
class User(Base):
    __tablename__ = "users" 

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    promo = Column(String, default="True")
    
    # To'g'rilandi: Shunchaki satr emas, bazada ustun bo'lishi shart!
    language = Column(String(10), default="uz", nullable=False)
    theme = Column(String(20), default="dark", nullable=False)
    
    scoin = Column(Integer, default=0)
    xp = Column(Integer, default=0)
    background = Column(String(), default="/static/images/default_bg.png")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Barcha aloqalar (Relationships) - To'g'ri sinxronizatsiya qilindi
    scoin_history = relationship("ScoinHistory", back_populates="user", cascade="all, delete-orphan")
    telegram_accounts = relationship("TelegramAccount", back_populates="user", cascade="all, delete-orphan")
    test_results = relationship("TestResult", back_populates="user", cascade="all, delete-orphan")
    tests = relationship("Tests", back_populates="creator", cascade="all, delete-orphan")
    allowed_tests = relationship("UserAllowedTest", back_populates="user", cascade="all, delete-orphan")


# ==========================================
# 2. USER TOKEN MODEL
# ==========================================
class UserToken(Base):
    __tablename__ = "user_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(255), unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    ip_address = Column(String(45), index=True) 
    created_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


# ==========================================
# 3. TESTS & QUESTIONS MODELS
# ==========================================
class Tests(Base):
    __tablename__ = "tests"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    is_public = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String(20), default="pending", nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Aloqalar
    creator = relationship("User", back_populates="tests")
    questions = relationship("Questions", back_populates="test", cascade="all, delete-orphan")
    allowed_users = relationship("UserAllowedTest", back_populates="test", cascade="all, delete-orphan")


class Questions(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(Integer, ForeignKey("tests.id", ondelete="CASCADE"), nullable=False)
    question_text = Column(Text, nullable=False)
    option_a = Column(Text, nullable=False)
    option_b = Column(Text, nullable=False)
    option_c = Column(Text, nullable=False)
    option_d = Column(Text, nullable=False)
    correct_answer = Column(CHAR(1), nullable=False) # 'A', 'B', 'C', 'D' 

    # Aloqalar
    test = relationship("Tests", back_populates="questions")


# ==========================================
# 4. SCOIN HISTORY MODEL & SERVICE
# ==========================================
class ScoinHistory(Base):
    __tablename__ = "scoin_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    amount = Column(Integer, nullable=False)  
    description = Column(String(255), nullable=False)  
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="scoin_history")


async def log_scoin_transaction(user_id: int, amount: int, description: str, db: AsyncSession):
    new_log = ScoinHistory(user_id=user_id, amount=amount, description=description)
    db.add(new_log)
    await db.flush()  

    from sqlalchemy import select
    q = select(ScoinHistory).where(ScoinHistory.user_id == user_id).order_by(desc(ScoinHistory.created_at))
    result = await db.execute(q)
    history_list = result.scalars().all()

    if len(history_list) > 10:
        excess_logs = history_list[10:]  
        for old_log in excess_logs:
            await db.delete(old_log)


# ==========================================
# 5. TEST RESULT MODEL (Mustaqil variant)
# ==========================================
class TestResult(Base):
    __tablename__ = "test_results"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    # KASKAD UZILDI: Oddiy Integer ustun, Tests jadvaliga bog'liq joyi yo'q!
    test_id = Column(Integer, nullable=False, index=True) 
    
    correct_answers = Column(Integer, nullable=False)  
    total_questions = Column(Integer, nullable=False)  
    percentage = Column(Float, nullable=False)         
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    user = relationship("User", back_populates="test_results")


# ==========================================
# 6. AI LEARNING ANALYSIS MODEL (Mustaqil variant)
# ==========================================
class AILearningAnalysis(Base):
    __tablename__ = "ai_learning_analysis"

    id = Column(Integer, primary_key=True, index=True)

    # KASKAD UZILDI: Test o'chsa ham ushbu ID omon qoladi
    test_id = Column(Integer, nullable=False, index=True) 
    
    analysis_text = Column(Text, nullable=False)  # AI pedagogik xulosasi
    analysis_questions = Column(Text, nullable=False)  # String formatdagi savollar arxivi (O'quvchi ilovasi uchun)
    generated_at = Column(DateTime(timezone=True), server_default=func.now())


async def clean_old_test_results(db: AsyncSession):
    from sqlalchemy import delete
    one_year_ago = datetime.now(timezone.utc) - timedelta(days=365)
    q = delete(TestResult).where(TestResult.created_at < one_year_ago)
    try:
        result = await db.execute(q)
        await db.commit()
        print(f"[CRON] {result.rowcount} ta 1 yillik eski test natijalari tozalandi.")
    except Exception as e:
        await db.rollback()
        print(f"[ERROR] Eski natijalarni tozalashda xato: {e}")



# ==========================================
# 7. USER ALLOWED TEST MODEL (PRIVATE TESTS)
# ==========================================
class UserAllowedTest(Base):
    __tablename__ = "user_allowed_tests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    # To'g'rilandi: ForeignKey endi to'g'ri 'tests.id' ga qaraydi
    test_id = Column(Integer, ForeignKey("tests.id", ondelete="CASCADE"), nullable=False)
    allowed_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="allowed_tests")
    test = relationship("Tests", back_populates="allowed_users")


# ==========================================
# 8. TELEGRAM ACCOUNT MODEL
# ==========================================
class TelegramAccount(Base):
    __tablename__ = "telegram_accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    tg_id = Column(String(55), unique=True, nullable=False, index=True) 
    username = Column(String(255), nullable=True)                      
    first_name = Column(String(255), nullable=False)                    
    last_name = Column(String(255), nullable=True)                     
    
    is_active = Column(Boolean, default=True, nullable=False)          
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="telegram_accounts")


# models.py
class UserOptions(Base):
    __tablename__ = "user_options"
    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(Integer, ForeignKey("tests.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    options = Column(String, default="[]") # [{"q_id": 1, "ans": "A"}, ...]
    end = Column(Boolean, default=False)