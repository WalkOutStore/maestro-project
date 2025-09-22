from typing import Any, List, Dict, Optional
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.campaign import Campaign
from app.api.endpoints.users import get_current_active_user
from app.database import get_db
from app.core.transparent_mentor import DecisionExplainer, DataVisualizer


router = APIRouter()


@router.post("/explain-prediction", response_model=Dict[str, Any])
def explain_prediction(
    prediction_data: Dict[str, Any],
    model_type: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    تفسير تنبؤ من نموذج التعلم الآلي
    """
    # إنشاء شارح القرارات
    explainer = DecisionExplainer(db)
    
    # تفسير التنبؤ
    explanation = explainer.explain_prediction(prediction_data, model_type)
    
    return explanation


@router.post("/explain-recommendation", response_model=Dict[str, Any])
def explain_recommendation(
    recommendation_data: Dict[str, Any],
    recommendation_type: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    تفسير توصية من النظام
    """
    # إنشاء شارح القرارات
    explainer = DecisionExplainer(db)
    
    # تفسير التوصية
    explanation = explainer.explain_recommendation(recommendation_data, recommendation_type)
    
    return explanation


@router.post("/generate-alternative-scenarios", response_model=List[Dict[str, Any]])
def generate_alternative_scenarios(
    base_data: Dict[str, Any],
    scenario_type: str,
    num_scenarios: int = 3,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    توليد سيناريوهات بديلة لمساعدة المستخدم في فهم تأثير التغييرات
    """
    # التحقق من وجود الحملة إذا تم تحديد معرف الحملة
    if "campaign_id" in base_data:
        campaign = db.query(Campaign).filter(
            Campaign.id == base_data["campaign_id"],
            Campaign.user_id == current_user.id
        ).first()
        
        if not campaign:
            raise HTTPException(status_code=404, detail="الحملة غير موجودة")
    
    # إنشاء شارح القرارات
    explainer = DecisionExplainer(db)
    
    # توليد السيناريوهات البديلة
    scenarios = explainer.generate_alternative_scenarios(base_data, scenario_type, num_scenarios)
    
    return scenarios


@router.post("/generate-visualization-config", response_model=Dict[str, Any])
def generate_visualization_config(
    data: Dict[str, Any],
    visualization_type: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    توليد تكوين التصور المرئي بناءً على نوع التصور والبيانات
    """
    # إنشاء مصور البيانات
    visualizer = DataVisualizer(db)
    
    # توليد تكوين التصور المرئي
    config = visualizer.generate_visualization_config(data, visualization_type)
    
    return config


@router.post("/generate-decision-path-visualization", response_model=Dict[str, Any])
def generate_decision_path_visualization(
    decision_path: List[Dict[str, Any]],
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    توليد تصور مرئي لمسار القرار
    """
    # إنشاء مصور البيانات
    visualizer = DataVisualizer(db)
    
    # توليد تصور مرئي لمسار القرار
    visualization = visualizer.generate_decision_path_visualization(decision_path)
    
    return visualization


@router.post("/generate-comparison-visualization", response_model=Dict[str, Any])
def generate_comparison_visualization(
    scenarios: List[Dict[str, Any]],
    metrics: List[str],
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    توليد تصور مرئي لمقارنة السيناريوهات
    """
    # إنشاء مصور البيانات
    visualizer = DataVisualizer(db)
    
    # توليد تصور مرئي لمقارنة السيناريوهات
    visualization = visualizer.generate_comparison_visualization(scenarios, metrics)
    
    return visualization
