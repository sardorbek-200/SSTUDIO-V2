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
    shop_history = relationship("ShopHistory", back_populates="user", cascade="all, delete-orphan")
    telegram_accounts = relationship("TelegramAccount", back_populates="user", cascade="all, delete-orphan")
    test_results = relationship("TestResult", back_populates="user", cascade="all, delete-orphan", lazy="selectin")
    tests = relationship("Tests", back_populates="creator", cascade="all, delete-orphan")
    allowed_tests = relationship("UserAllowedTest", back_populates="user", cascade="all, delete-orphan")
    status = relationship("Status", back_populates="user", cascade="all, delete-orphan", uselist=False)


# ==========================================
# 2. USER STATUS MODEL
# ==========================================
class Status(Base):
    __tablename__ = "user_statuses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    rank = Column(String(100), nullable=False)
    picture = Column(String(255), nullable=True)
    animation = Column(String(255), nullable=True)
    color = Column(String(50), nullable=True)
    rank_color = Column(String(20), nullable=True)

    user = relationship("User", back_populates="status")


# ==========================================
# 3. SHOP RANK MODEL
# ==========================================
class ShopRank(Base):
    __tablename__ = "shop_ranks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Integer, nullable=False, default=0)
    picture = Column(String(255), nullable=True)
    name_color = Column(String(20), nullable=True)
    rank_color = Column(String(20), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)


# ==========================================
# 4. SHOP ANIMATION MODEL
# ==========================================
class ShopAnimation(Base):
    __tablename__ = "shop_animations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Integer, nullable=False, default=0)
    css_code = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)


# ==========================================
# 5. SHOP COLOR MODEL
# ==========================================
class ShopColor(Base):
    __tablename__ = "shop_colors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Integer, nullable=False, default=0)
    name = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)


# ==========================================
# 6. SHOP BACKGROUND MODEL
# ==========================================
class ShopBackground(Base):
    __tablename__ = "shop_backgrounds"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Integer, nullable=False, default=0)
    picture = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)


# ==========================================
# 7. SHOP HISTORY MODEL
# ==========================================
class ShopHistory(Base):
    __tablename__ = "shop_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    item_type = Column(String(50), nullable=False)
    item_id = Column(Integer, nullable=False)
    item_name = Column(String(255), nullable=False)
    price = Column(Integer, nullable=False)
    details = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="shop_history")


# ==========================================
# 8. USER TOKEN MODEL
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
    user = relationship("User", back_populates="test_results", lazy="selectin")
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

# ==========================================
# 9. ADMIN MODEL
# ==========================================
class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    # Admin bo'lish uchun avval User jadvalida mavjud bo'lishi kerak
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    added_at = Column(DateTime(timezone=True), server_default=func.now())

    # User bilan bog'lanish
    user = relationship("User", backref="admin_profile")