from typing import Any, List, Dict, Optional
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.campaign import Campaign
from app.models.knowledge_base import KnowledgeRule, MLModel
from app.api.endpoints.users import get_current_active_user
from app.database import get_db
from app.core.strategic_mind import DynamicKnowledgeBase, HybridInferenceEngine
from app import schemas


router = APIRouter()


@router.post("/predict-ctr", response_model=Dict[str, Any])
def predict_ctr(
    campaign_data: Dict[str, Any],
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    التنبؤ بمعدل النقر إلى الظهور (CTR) للحملة
    """
    print(f"🔍 DEBUG: predict_ctr endpoint called")
    print(f"🔍 DEBUG: campaign_data: {campaign_data}")
    print(f"🔍 DEBUG: current_user: {current_user.id if current_user else 'None'}")

    # التحقق من وجود الحملة إذا تم تحديد معرف الحملة
    if "campaign_id" in campaign_data:
        campaign = db.query(Campaign).filter(
            Campaign.id == campaign_data["campaign_id"],
            Campaign.user_id == current_user.id
        ).first()

        if not campaign:
            print(f"❌ DEBUG: Campaign not found")
            raise HTTPException(status_code=404, detail="الحملة غير موجودة")

    # إنشاء محرك الاستدلال
    inference_engine = HybridInferenceEngine(db)

    # التنبؤ بمعدل النقر إلى الظهور
    prediction = inference_engine.predict_ctr(campaign_data)

    print(f"✅ DEBUG: prediction result: {prediction}")
    return prediction


@router.post("/predict-roi", response_model=Dict[str, Any])
def predict_roi(
    campaign_data: Dict[str, Any],
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    التنبؤ بالعائد على الاستثمار (ROI) للحملة
    """
    # التحقق من وجود الحملة إذا تم تحديد معرف الحملة
    if "campaign_id" in campaign_data:
        campaign = db.query(Campaign).filter(
            Campaign.id == campaign_data["campaign_id"],
            Campaign.user_id == current_user.id
        ).first()
        
        if not campaign:
            raise HTTPException(status_code=404, detail="الحملة غير موجودة")
    
    # إنشاء محرك الاستدلال
    inference_engine = HybridInferenceEngine(db)
    
    # التنبؤ بالعائد على الاستثمار
    prediction = inference_engine.predict_roi(campaign_data)
    
    return prediction


@router.post("/recommend-channels", response_model=List[Dict[str, Any]])
def recommend_channels(
    campaign_data: Dict[str, Any],
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    توصية بقنوات التسويق المناسبة للحملة
    """
    # التحقق من وجود الحملة إذا تم تحديد معرف الحملة
    if "campaign_id" in campaign_data:
        campaign = db.query(Campaign).filter(
            Campaign.id == campaign_data["campaign_id"],
            Campaign.user_id == current_user.id
        ).first()
        
        if not campaign:
            raise HTTPException(status_code=404, detail="الحملة غير موجودة")
    
    # إنشاء محرك الاستدلال
    inference_engine = HybridInferenceEngine(db)
    
    # توصية بقنوات التسويق
    recommendations = inference_engine.recommend_channels(campaign_data)
    
    return recommendations


@router.get("/knowledge-rules", response_model=List[Dict[str, Any]])
def get_knowledge_rules(
    rule_type: Optional[str] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    الحصول على قواعد المعرفة
    """
    # إنشاء قاعدة المعرفة
    knowledge_base = DynamicKnowledgeBase(db)
    
    # الحصول على القواعد
    rules = knowledge_base.get_rules(rule_type)
    
    return rules


@router.post("/knowledge-rules", response_model=Dict[str, Any])
def create_knowledge_rule(
    rule: schemas.KnowledgeRuleCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    إنشاء قاعدة معرفية جديدة
    """
    # التحقق من صلاحيات المستخدم
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="ليس لديك صلاحية لإنشاء قواعد معرفية")
    
    # إنشاء قاعدة المعرفة
    knowledge_base = DynamicKnowledgeBase(db)
    
    # إنشاء القاعدة
    rule_db = knowledge_base.add_rule(rule)
    
    if not rule_db:
        raise HTTPException(status_code=400, detail="فشل إنشاء القاعدة")
    
    return {
        "id": rule_db.id,
        "name": rule_db.name,
        "rule_type": rule_db.rule_type,
        "conditions": rule_db.conditions,
        "actions": rule_db.actions,
        "priority": rule_db.priority
    }


@router.post("/evaluate-rules", response_model=List[Dict[str, Any]])
def evaluate_rules(
    context: Dict[str, Any],
    rule_type: Optional[str] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    تقييم القواعد على سياق معين
    """
    # إنشاء قاعدة المعرفة
    knowledge_base = DynamicKnowledgeBase(db)
    
    # تقييم القواعد
    actions = knowledge_base.evaluate_rules(context, rule_type)
    
    return actions


@router.post("/update-from-feedback", response_model=Dict[str, bool])
def update_from_feedback(
    feedback_data: Dict[str, Any],
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    تحديث النماذج بناءً على التغذية الراجعة
    """
    # إنشاء محرك الاستدلال
    inference_engine = HybridInferenceEngine(db)
    
    # تحديث النماذج
    success = inference_engine.update_from_feedback(feedback_data)
    
    return {"success": success}
