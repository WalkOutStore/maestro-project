from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import os

from app.api.api import api_router
from app.config import settings
from app.database import Base, engine


# إنشاء جداول قاعدة البيانات
Base.metadata.create_all(bind=engine)

# إنشاء تطبيق FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# إعداد CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# إضافة مسارات API
app.include_router(api_router, prefix=settings.API_V1_STR)

# إضافة مجلد الملفات الثابتة إذا كان موجودًا
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/")
def root():
    """
    جذر التطبيق
    """
    return {
        "message": "مرحبًا بك في منصة Maestro للتسويق الرقمي المدعومة بالذكاء الاصطناعي",
        "version": "1.0.0",
        "docs_url": "/docs"
    }


@app.get("/health")
def health_check():
    """
    فحص صحة التطبيق
    """
    return {
        "status": "ok",
        "api_version": "v1"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
