import os
from pydantic_settings import BaseSettings
from typing import Optional, Dict, Any, List


class Settings(BaseSettings):
    """
    إعدادات التطبيق - Maestro AI Marketing Platform
    """
    # إعدادات عامة
    PROJECT_NAME: str = "Maestro AI Marketing Platform"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = True

    # إعدادات قاعدة البيانات
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./maestro.db")

    # إعدادات الأمان
    SECRET_KEY: str = os.getenv("SECRET_KEY", "") # يجب استبدالها بمفتاح سري حقيقي
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 أيام

    # ========================================
    # 🔑 إعدادات API خارجية (مطلوبة للوظائف الحقيقية)
    # ========================================

    # GROQ API - لتوليد النصوص الإبداعية
    # احصل على المفتاح من: https://console.groq.com/keys
    GROQ_API_KEY: Optional[str] = os.getenv("GROQ_API_KEY", "") # أدخل مفتاح GROQ API الحقيقي هنا
    # GOOGLE_TRENDS_API_KEY: Optional[str] = os.getenv("GOOGLE_TRENDS_API_KEY", "")
    # # Google Trends API - لتحليل اتجاهات البحث (pytrends لا يستخدم مفتاح API مباشر)
    # # Twitter API
    # TWITTER_API_KEY: Optional[str] = os.getenv("TWITTER_API_KEY", "")
    # TWITTER_API_SECRET: Optional[str] = os.getenv("TWITTER_API_SECRET", "")
    # TWITTER_ACCESS_TOKEN: Optional[str] = os.getenv("TWITTER_ACCESS_TOKEN", "")
    # TWITTER_ACCESS_SECRET: Optional[str] = os.getenv("TWITTER_ACCESS_SECRET", "")


    # إعدادات نماذج التعلم الآلي
    ML_MODELS_PATH: str = os.getenv("ML_MODELS_PATH", "./ml_models")

    # إعدادات CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://localhost:5173",
        "https://maestro-marketing.com",
    ]

    # ========================================
    # 🔧 إعدادات متقدمة
    # ========================================

    # إعدادات التخزين المؤقت (Cache)
    CACHE_DURATION_HOURS: int = int(os.getenv("CACHE_DURATION_HOURS", "24"))
    REDIS_URL: Optional[str] = os.getenv("REDIS_URL", None)

    # إعدادات مراقبة الأداء
    ENABLE_PERFORMANCE_MONITORING: bool = os.getenv("ENABLE_PERFORMANCE_MONITORING", "false").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # إعدادات معالجة البيانات
    MAX_TREND_KEYWORDS: int = int(os.getenv("MAX_TREND_KEYWORDS", "10"))
    MIN_TREND_CONFIDENCE: float = float(os.getenv("MIN_TREND_CONFIDENCE", "0.3"))

    class Config:
        env_file = ".env"
        case_sensitive = True

    def validate_api_keys(self) -> Dict[str, bool]:
        """
        التحقق من صحة مفاتيح API المطلوبة مع تفاصيل إضافية
        """
        validation = {
            "groq_api": bool(self.GROQ_API_KEY and self.GROQ_API_KEY != ""),
    #         "google_trends_api": bool(self.GOOGLE_TRENDS_API_KEY),
    # "twitter_api": all([
    #     self.TWITTER_API_KEY,
    #     self.TWITTER_API_SECRET,
    #     self.TWITTER_ACCESS_TOKEN,
    #     self.TWITTER_ACCESS_SECRET
    # ])
        }

        # طباعة حالة كل API مع تفاصيل إضافية
        print("🔑 API Keys Validation:")
        print(f"  • GROQ API: {'✅ Configured' if validation['groq_api'] else '❌ Missing'}")
        if not validation['groq_api']:
            print("    💡 Get your API key from: https://console.groq.com/keys")



        return validation

    def get_missing_apis(self) -> List[str]:
        """
        الحصول على قائمة بـ APIs المفقودة مع تفاصيل الإعداد
        """
        validation = self.validate_api_keys()
        missing = []

        if not validation['groq_api']:
            missing.append("GROQ API (for text generation) - Get key from: https://console.groq.com/keys")



        return missing

    def get_api_status_summary(self) -> Dict[str, Any]:
        """
        الحصول على ملخص حالة جميع الـ APIs
        """
        validation = self.validate_api_keys()
        missing_apis = self.get_missing_apis()

        return {
            "total_apis": 2,
            "configured_apis": sum(validation.values()),
            "missing_apis": len(missing_apis),
            "missing_apis_list": missing_apis,
            "validation_details": validation,
            "ready_for_production": sum(validation.values()) == 3
        }

    def validate_and_setup(self) -> bool:
        """
        التحقق من الإعداد والتأكد من الجاهزية للاستخدام
        """
        print("🚀 Starting Maestro API Configuration Validation...")
        print("=" * 60)

        status = self.get_api_status_summary()

        if status["ready_for_production"]:
            print("✅ All APIs are properly configured!")
            print("🎯 System is ready for production use with real data.")
        else:
            print(f"⚠️ Missing {status['missing_apis']} API configurations:")
            for missing_api in status["missing_apis_list"]:
                print(f"  • {missing_api}")
            print("💡 Please configure the missing APIs for full functionality.")

        print("=" * 60)
        return status["ready_for_production"]


settings = Settings()