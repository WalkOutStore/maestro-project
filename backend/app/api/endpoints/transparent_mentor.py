from typing import Any, Dict, List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.endpoints.users import get_current_active_user
from app.database import get_db
from app.core.creative_spark import TransparentMentor, TextGenerator

router = APIRouter()


@router.post("/explain-generation", response_model=Dict[str, Any])
def explain_content_generation(
    campaign_data: Dict[str, Any],
    content_type: str = "ad_copy",
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    شرح كيفية توليد المحتوى واتخاذ القرارات
    """
    transparent_mentor = TransparentMentor(db)

    # توليد المحتوى أولاً
    ad_copies = transparent_mentor.generate_content(campaign_data, content_type)

    # تفسير عملية التوليد لكل نسخة محتوى
    explanations = [
        transparent_mentor.explain_content_generation(campaign_data, ad_copy)
        for ad_copy in ad_copies
    ]

    return {
        "content_results": ad_copies,
        "explanations": explanations,
        "summary": {
            "total_results": len(ad_copies),
            "sources_used": list({r.get("source") for r in ad_copies}),
            "avg_confidence": sum([r.get("confidence", 0) for r in ad_copies]) / len(ad_copies) if ad_copies else 0
        }
    }


@router.post("/explain-prediction", response_model=List[Dict[str, Any]])
def explain_prediction(prediction_data: Any, model_type: str, db: Session = Depends(get_db)):
    mentor = TransparentMentor(db)
    
    # التأكد من نوع البيانات
    if isinstance(prediction_data, list):
        prediction_data = prediction_data[0]
    
    # استخدام دالة موجودة لتفسير التنبؤات
    explanation = mentor._analyze_confidence_factors(prediction_data)
    
    # إرجاع قائمة لتتناسب مع الواجهة الأمامية
    return explanation


@router.post("/generate-alternative-scenarios", response_model=List[Dict[str, Any]])
def generate_alternative_scenarios(
    base_data: Dict[str, Any],
    scenario_type: str = Query(..., description="نوع السيناريو"),
    num_scenarios: int = Query(3, description="عدد السيناريوهات"),
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    توليد سيناريوهات بديلة
    """
    mentor = TransparentMentor(db)

    # استخراج بيانات الحملة من base_data
    campaign_data = base_data.get("base", base_data)
    # إضافة بيانات افتراضية إذا لم تكن موجودة
    if "industry" not in campaign_data:
        campaign_data["industry"] = "technology"
    if "product_name" not in campaign_data:
        campaign_data["product_name"] = "منتج تجريبي"

    text_generator = TextGenerator(db)
    ad_copies = text_generator.generate_ad_copy(campaign_data, "ad_copy")

    # توليد بدائل
    alternatives = mentor._generate_alternatives(base_data, ad_copies)

    # تحويل إلى قائمة للعرض
    scenarios = []
    for key, value in alternatives.items():
        if isinstance(value, list):
            for item in value:
                scenarios.append({
                    "type": key,
                    "scenario": item.get("description", str(item)),
                    "expected_benefit": item.get("expected_benefit", ""),
                    "implementation_effort": item.get("implementation_effort", "")
                })

    return scenarios[:num_scenarios]
