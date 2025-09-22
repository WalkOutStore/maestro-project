from typing import Any, List, Dict, Optional
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.campaign import Campaign, Recommendation
from app.api.endpoints.users import get_current_active_user
from app.database import get_db
from app.core.learning_loop import FeedbackProcessor, ModelUpdater


router = APIRouter()


@router.post("/save-recommendation-feedback", response_model=Dict[str, bool])
def save_recommendation_feedback(
    feedback_data: Dict[str, Any],
    recommendation_id: int = Query(..., title="معرف التوصية"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    حفظ التغذية الراجعة على توصية
    """
    # التحقق من وجود التوصية
    recommendation = db.query(Recommendation).filter(Recommendation.id == recommendation_id).first()
    
    if not recommendation:
        raise HTTPException(status_code=404, detail="التوصية غير موجودة")
    
    # التحقق من ملكية الحملة
    campaign = db.query(Campaign).filter(
        Campaign.id == recommendation.campaign_id,
        Campaign.user_id == current_user.id
    ).first()
    
    if not campaign:
        raise HTTPException(status_code=403, detail="ليس لديك صلاحية للوصول إلى هذه التوصية")
    
    # إنشاء معالج التغذية الراجعة
    feedback_processor = FeedbackProcessor(db)
    
    # حفظ التغذية الراجعة
    success = feedback_processor.save_recommendation_feedback(recommendation_id, feedback_data)
    
    return {"success": success}


@router.get("/recommendation-feedback-stats", response_model=Dict[str, Any])
def get_recommendation_feedback_stats(
    campaign_id: Optional[int] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    الحصول على إحصائيات التغذية الراجعة للتوصيات
    """
    # التحقق من وجود الحملة إذا تم تحديد معرف الحملة
    if campaign_id:
        campaign = db.query(Campaign).filter(
            Campaign.id == campaign_id,
            Campaign.user_id == current_user.id
        ).first()
        
        if not campaign:
            raise HTTPException(status_code=404, detail="الحملة غير موجودة")
    
    # إنشاء معالج التغذية الراجعة
    feedback_processor = FeedbackProcessor(db)
    
    # الحصول على إحصائيات التغذية الراجعة
    stats = feedback_processor.get_recommendation_feedback_stats(campaign_id)
    
    return stats


@router.post("/collect-user-interactions", response_model=Dict[str, bool])
def collect_user_interactions(
    interaction_data: Dict[str, Any],
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    جمع تفاعلات المستخدم مع النظام
    """
    # إنشاء معالج التغذية الراجعة
    feedback_processor = FeedbackProcessor(db)
    
    # جمع تفاعلات المستخدم
    success = feedback_processor.collect_user_interactions(current_user.id, interaction_data)
    
    return {"success": success}


@router.get("/analyze-feedback-trends", response_model=Dict[str, Any])
def analyze_feedback_trends(
    days: int = 30,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    تحليل اتجاهات التغذية الراجعة على مدار فترة زمنية
    """
    # التحقق من صلاحيات المستخدم
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="ليس لديك صلاحية للوصول إلى هذه البيانات")
    
    # إنشاء معالج التغذية الراجعة
    feedback_processor = FeedbackProcessor(db)
    
    # تحليل اتجاهات التغذية الراجعة
    trends = feedback_processor.analyze_feedback_trends(days)
    
    return trends


@router.post("/update-model", response_model=Dict[str, Any])
def update_model(
    model_type: str,
    update_params: Optional[Dict[str, Any]] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    تحديث نموذج التعلم الآلي بناءً على التغذية الراجعة
    """
    # التحقق من صلاحيات المستخدم
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="ليس لديك صلاحية لتحديث النماذج")
    
    # إنشاء محدث النماذج
    model_updater = ModelUpdater(db)
    
    # تحديث النموذج
    result = model_updater.update_model(model_type, update_params)
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result


@router.post("/schedule-model-update", response_model=Dict[str, Any])
def schedule_model_update(
    model_type: str,
    schedule: Dict[str, Any],
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    جدولة تحديث النموذج
    """
    # التحقق من صلاحيات المستخدم
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="ليس لديك صلاحية لجدولة تحديث النماذج")
    
    # إنشاء محدث النماذج
    model_updater = ModelUpdater(db)
    
    # جدولة تحديث النموذج
    result = model_updater.schedule_model_update(model_type, schedule)
    
    return result
