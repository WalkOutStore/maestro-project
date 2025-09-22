from typing import Any, List, Dict, Optional
from fastapi import APIRouter, Depends, HTTPException, Path, Query, UploadFile, File
from sqlalchemy.orm import Session
import os

from app.models.user import User
from app.models.campaign import Campaign
from app.models.knowledge_base import ContentTemplate
from app.api.endpoints.users import get_current_active_user
from app.database import get_db
from app.core.creative_spark import TextGenerator, VisualSuggestions, TrendAnalyzer
from app.utils import sanitize_filename, ensure_dir
from app.config import settings


router = APIRouter()


@router.post("/generate-ad-copy", response_model=List[Dict[str, Any]])
def generate_ad_copy(
    campaign_data: Dict[str, Any],
    content_type: str = "ad_copy",
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    توليد نص إعلاني بناءً على بيانات الحملة
    """
    # التحقق من وجود الحملة إذا تم تحديد معرف الحملة
    if "campaign_id" in campaign_data:
        campaign = db.query(Campaign).filter(
            Campaign.id == campaign_data["campaign_id"],
            Campaign.user_id == current_user.id
        ).first()
        
        if not campaign:
            raise HTTPException(status_code=404, detail="الحملة غير موجودة")
    
    # إنشاء مولد النصوص
    text_generator = TextGenerator(db)
    
    # توليد النص الإعلاني
    ad_copies = text_generator.generate_ad_copy(campaign_data, content_type)
    
    return ad_copies


@router.post("/generate-visual-suggestions", response_model=List[Dict[str, Any]])
def generate_visual_suggestions(
    campaign_data: Dict[str, Any],
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    توليد اقتراحات بصرية بناءً على بيانات الحملة
    """
    # التحقق من وجود الحملة إذا تم تحديد معرف الحملة
    if "campaign_id" in campaign_data:
        campaign = db.query(Campaign).filter(
            Campaign.id == campaign_data["campaign_id"],
            Campaign.user_id == current_user.id
        ).first()
        
        if not campaign:
            raise HTTPException(status_code=404, detail="الحملة غير موجودة")
    
    # إنشاء نظام الاقتراحات البصرية
    visual_suggestions = VisualSuggestions(db)
    
    # توليد الاقتراحات البصرية
    suggestions = visual_suggestions.generate_visual_suggestions(campaign_data)
    
    return suggestions


@router.post("/analyze-image", response_model=Dict[str, Any])
async def analyze_image(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    تحليل صورة باستخدام نموذج CLIP
    """
    # التحقق من نوع الملف
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="الملف ليس صورة")
    
    # إنشاء مجلد التحميل إذا لم يكن موجودًا
    upload_dir = os.path.join(settings.ML_MODELS_PATH, "uploads")
    ensure_dir(upload_dir)
    
    # حفظ الملف
    filename = sanitize_filename(file.filename)
    file_path = os.path.join(upload_dir, filename)
    
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    # إنشاء نظام الاقتراحات البصرية
    visual_suggestions = VisualSuggestions(db)
    
    # تحليل الصورة
    analysis = visual_suggestions.analyze_image(file_path)
    
    # إضافة مسار الملف إلى النتيجة
    analysis["file_path"] = file_path
    
    return analysis


@router.post("/analyze-trends", response_model=Dict[str, Any])
def analyze_trends(
    campaign_data: Dict[str, Any],
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    تحليل الاتجاهات ذات الصلة بالحملة
    """
    # التحقق من وجود الحملة إذا تم تحديد معرف الحملة
    if "campaign_id" in campaign_data:
        campaign = db.query(Campaign).filter(
            Campaign.id == campaign_data["campaign_id"],
            Campaign.user_id == current_user.id
        ).first()
        
        if not campaign:
            raise HTTPException(status_code=404, detail="الحملة غير موجودة")
    
    # إنشاء محلل الاتجاهات
    trend_analyzer = TrendAnalyzer(db)
    
    # تحليل الاتجاهات
    analysis = trend_analyzer.analyze_trends(campaign_data)
    
    return analysis


@router.get("/content-templates", response_model=List[Dict[str, Any]])
def get_content_templates(
    content_type: Optional[str] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    الحصول على قوالب المحتوى
    """
    # إنشاء استعلام قاعدة البيانات
    query = db.query(ContentTemplate)
    
    # تصفية حسب نوع المحتوى إذا تم تحديده
    if content_type:
        query = query.filter(ContentTemplate.content_type == content_type)
    
    # تنفيذ الاستعلام
    templates = query.all()
    
    # تحويل النتائج إلى قاموس
    result = []
    for template in templates:
        result.append({
            "id": template.id,
            "name": template.name,
            "description": template.description,
            "content_type": template.content_type,
            "template_data": template.template_data,
            "variables": template.variables,
            "performance_score": template.performance_score
        })
    
    return result


@router.post("/content-templates", response_model=Dict[str, Any])
def create_content_template(
    template_data: Dict[str, Any],
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    إنشاء قالب محتوى جديد
    """
    # التحقق من صلاحيات المستخدم
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="ليس لديك صلاحية لإنشاء قوالب محتوى")
    
    # إنشاء مولد النصوص
    text_generator = TextGenerator(db)
    
    # إنشاء القالب
    template = text_generator.save_template(template_data)
    
    if not template:
        raise HTTPException(status_code=400, detail="فشل إنشاء القالب")
    
    return {
        "id": template.id,
        "name": template.name,
        "content_type": template.content_type,
        "template_data": template.template_data,
        "variables": template.variables,
        "performance_score": template.performance_score
    }


@router.put("/content-templates/{template_id}/performance", response_model=Dict[str, bool])
def update_template_performance(
    performance_data: Dict[str, float],
    template_id: int = Path(..., title="معرف القالب"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    تحديث درجة أداء القالب
    """
    # التحقق من وجود القالب
    template = db.query(ContentTemplate).filter(ContentTemplate.id == template_id).first()
    
    if not template:
        raise HTTPException(status_code=404, detail="القالب غير موجود")
    
    # التحقق من صلاحيات المستخدم
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="ليس لديك صلاحية لتحديث أداء القوالب")
    
    # إنشاء مولد النصوص
    text_generator = TextGenerator(db)
    
    # تحديث درجة الأداء
    success = text_generator.update_template_performance(template_id, performance_data.get("performance_score", 0.0))
    
    return {"success": success}
