from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
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

# إعداد الملفات الثابتة
static_dir = os.path.join(os.path.dirname(__file__), "static")
assets_dir = os.path.join(static_dir, "assets")

if os.path.exists(static_dir):
    # خدمة ملفات الأصول مباشرة
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# إضافة مسار للـ favicon
@app.get("/favicon.ico")
async def favicon():
    favicon_path = os.path.join(static_dir, "favicon.ico")
    if os.path.exists(favicon_path):
        from fastapi.responses import FileResponse
        return FileResponse(favicon_path)
    else:
        raise HTTPException(status_code=404, detail="Favicon not found")


@app.get("/")
async def serve_frontend():
    """
    خدمة ملف index.html للواجهة الأمامية
    """
    with open(os.path.join(static_dir, "index.html")) as f:
        return HTMLResponse(content=f.read())


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
