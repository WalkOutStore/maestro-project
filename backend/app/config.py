import os
from pydantic_settings import BaseSettings
from typing import Optional, Dict, Any, List


class Settings(BaseSettings):
    """
    إعدادات التطبيق
    """
    # إعدادات عامة
    PROJECT_NAME: str = "Maestro AI Marketing Platform"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = True
    
    # إعدادات قاعدة البيانات
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./maestro.db")
    
    # إعدادات الأمان
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 أيام
    
    # إعدادات API خارجية
    # OpenAI API - اتركها فارغة ليتم ملؤها لاحقًا
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY", "")
    
    # Google Trends API - اتركها فارغة ليتم ملؤها لاحقًا
    GOOGLE_TRENDS_API_KEY: Optional[str] = os.getenv("GOOGLE_TRENDS_API_KEY", "")
    
    # Twitter API - اتركها فارغة ليتم ملؤها لاحقًا
    TWITTER_API_KEY: Optional[str] = os.getenv("TWITTER_API_KEY", "")
    TWITTER_API_SECRET: Optional[str] = os.getenv("TWITTER_API_SECRET", "")
    TWITTER_ACCESS_TOKEN: Optional[str] = os.getenv("TWITTER_ACCESS_TOKEN", "")
    TWITTER_ACCESS_SECRET: Optional[str] = os.getenv("TWITTER_ACCESS_SECRET", "")
    
    # إعدادات نماذج التعلم الآلي
    ML_MODELS_PATH: str = os.getenv("ML_MODELS_PATH", "./ml_models")
    
    # إعدادات CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://localhost:5173",
        "https://maestro-marketing.com",
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
