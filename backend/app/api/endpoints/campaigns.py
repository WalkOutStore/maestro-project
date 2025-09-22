from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session

from app import schemas
from app.models.user import User
from app.models.campaign import Campaign, Content, Recommendation
from app.api.endpoints.users import get_current_active_user
from app.database import get_db


router = APIRouter()


@router.get("/", response_model=List[schemas.Campaign])
def read_campaigns(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    الحصول على قائمة الحملات التسويقية للمستخدم الحالي
    """
    # إنشاء استعلام قاعدة البيانات
    query = db.query(Campaign).filter(Campaign.user_id == current_user.id)
    
    # تصفية حسب الحالة إذا تم تحديدها
    if status:
        query = query.filter(Campaign.status == status)
    
    # تنفيذ الاستعلام مع التخطي والحد
    campaigns = query.offset(skip).limit(limit).all()
    
    return campaigns


@router.post("/", response_model=schemas.Campaign)
def create_campaign(
    campaign_in: schemas.CampaignCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    إنشاء حملة تسويقية جديدة
    """
    # إنشاء الحملة
    campaign = Campaign(
        name=campaign_in.name,
        description=campaign_in.description,
        status=campaign_in.status,
        budget=campaign_in.budget,
        start_date=campaign_in.start_date,
        end_date=campaign_in.end_date,
        target_audience=campaign_in.target_audience,
        channels=campaign_in.channels,
        user_id=current_user.id
    )
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    
    return campaign


@router.get("/{campaign_id}", response_model=schemas.CampaignWithDetails)
def read_campaign(
    campaign_id: int = Path(..., title="معرف الحملة"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    الحصول على حملة تسويقية محددة
    """
    # البحث عن الحملة
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id,
        Campaign.user_id == current_user.id
    ).first()
    
    if not campaign:
        raise HTTPException(status_code=404, detail="الحملة غير موجودة")
    
    return campaign


@router.put("/{campaign_id}", response_model=schemas.Campaign)
def update_campaign(
    campaign_in: schemas.CampaignUpdate,
    campaign_id: int = Path(..., title="معرف الحملة"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    تحديث حملة تسويقية
    """
    # البحث عن الحملة
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id,
        Campaign.user_id == current_user.id
    ).first()
    
    if not campaign:
        raise HTTPException(status_code=404, detail="الحملة غير موجودة")
    
    # تحديث البيانات
    if campaign_in.name is not None:
        campaign.name = campaign_in.name
    if campaign_in.description is not None:
        campaign.description = campaign_in.description
    if campaign_in.status is not None:
        campaign.status = campaign_in.status
    if campaign_in.budget is not None:
        campaign.budget = campaign_in.budget
    if campaign_in.start_date is not None:
        campaign.start_date = campaign_in.start_date
    if campaign_in.end_date is not None:
        campaign.end_date = campaign_in.end_date
    if campaign_in.target_audience is not None:
        campaign.target_audience = campaign_in.target_audience
    if campaign_in.channels is not None:
        campaign.channels = campaign_in.channels
    if campaign_in.metrics is not None:
        campaign.metrics = campaign_in.metrics
    
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    
    return campaign


@router.delete("/{campaign_id}")
def delete_campaign(
    campaign_id: int = Path(..., title="معرف الحملة"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    حذف حملة تسويقية
    """
    # البحث عن الحملة
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id,
        Campaign.user_id == current_user.id
    ).first()
    
    if not campaign:
        raise HTTPException(status_code=404, detail="الحملة غير موجودة")
    
    # حذف الحملة
    db.delete(campaign)
    db.commit()
    
    return {"message": "تم حذف الحملة بنجاح"}


# API للمحتوى

@router.get("/{campaign_id}/contents", response_model=List[schemas.Content])
def read_contents(
    campaign_id: int = Path(..., title="معرف الحملة"),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    الحصول على قائمة محتويات الحملة
    """
    # التحقق من وجود الحملة
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id,
        Campaign.user_id == current_user.id
    ).first()
    
    if not campaign:
        raise HTTPException(status_code=404, detail="الحملة غير موجودة")
    
    # الحصول على المحتويات
    contents = db.query(Content).filter(
        Content.campaign_id == campaign_id
    ).offset(skip).limit(limit).all()
    
    return contents


@router.post("/{campaign_id}/contents", response_model=schemas.Content)
def create_content(
    content_in: schemas.ContentCreate,
    campaign_id: int = Path(..., title="معرف الحملة"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    إنشاء محتوى جديد للحملة
    """
    # التحقق من وجود الحملة
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id,
        Campaign.user_id == current_user.id
    ).first()
    
    if not campaign:
        raise HTTPException(status_code=404, detail="الحملة غير موجودة")
    
    # إنشاء المحتوى
    content = Content(
        title=content_in.title,
        content_type=content_in.content_type,
        content_data=content_in.content_data,
        channel=content_in.channel,
        status=content_in.status,
        campaign_id=campaign_id
    )
    db.add(content)
    db.commit()
    db.refresh(content)
    
    return content


@router.put("/{campaign_id}/contents/{content_id}", response_model=schemas.Content)
def update_content(
    content_in: schemas.ContentUpdate,
    campaign_id: int = Path(..., title="معرف الحملة"),
    content_id: int = Path(..., title="معرف المحتوى"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    تحديث محتوى الحملة
    """
    # التحقق من وجود الحملة
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id,
        Campaign.user_id == current_user.id
    ).first()
    
    if not campaign:
        raise HTTPException(status_code=404, detail="الحملة غير موجودة")
    
    # البحث عن المحتوى
    content = db.query(Content).filter(
        Content.id == content_id,
        Content.campaign_id == campaign_id
    ).first()
    
    if not content:
        raise HTTPException(status_code=404, detail="المحتوى غير موجود")
    
    # تحديث البيانات
    if content_in.title is not None:
        content.title = content_in.title
    if content_in.content_type is not None:
        content.content_type = content_in.content_type
    if content_in.content_data is not None:
        content.content_data = content_in.content_data
    if content_in.channel is not None:
        content.channel = content_in.channel
    if content_in.status is not None:
        content.status = content_in.status
    if content_in.performance is not None:
        content.performance = content_in.performance
    
    db.add(content)
    db.commit()
    db.refresh(content)
    
    return content


@router.delete("/{campaign_id}/contents/{content_id}")
def delete_content(
    campaign_id: int = Path(..., title="معرف الحملة"),
    content_id: int = Path(..., title="معرف المحتوى"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    حذف محتوى الحملة
    """
    # التحقق من وجود الحملة
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id,
        Campaign.user_id == current_user.id
    ).first()
    
    if not campaign:
        raise HTTPException(status_code=404, detail="الحملة غير موجودة")
    
    # البحث عن المحتوى
    content = db.query(Content).filter(
        Content.id == content_id,
        Content.campaign_id == campaign_id
    ).first()
    
    if not content:
        raise HTTPException(status_code=404, detail="المحتوى غير موجود")
    
    # حذف المحتوى
    db.delete(content)
    db.commit()
    
    return {"message": "تم حذف المحتوى بنجاح"}


# API للتوصيات

@router.get("/{campaign_id}/recommendations", response_model=List[schemas.Recommendation])
def read_recommendations(
    campaign_id: int = Path(..., title="معرف الحملة"),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    الحصول على قائمة توصيات الحملة
    """
    # التحقق من وجود الحملة
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id,
        Campaign.user_id == current_user.id
    ).first()
    
    if not campaign:
        raise HTTPException(status_code=404, detail="الحملة غير موجودة")
    
    # الحصول على التوصيات
    recommendations = db.query(Recommendation).filter(
        Recommendation.campaign_id == campaign_id
    ).offset(skip).limit(limit).all()
    
    return recommendations


@router.post("/{campaign_id}/recommendations", response_model=schemas.Recommendation)
def create_recommendation(
    recommendation_in: schemas.RecommendationCreate,
    campaign_id: int = Path(..., title="معرف الحملة"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    إنشاء توصية جديدة للحملة
    """
    # التحقق من وجود الحملة
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id,
        Campaign.user_id == current_user.id
    ).first()
    
    if not campaign:
        raise HTTPException(status_code=404, detail="الحملة غير موجودة")
    
    # إنشاء التوصية
    recommendation = Recommendation(
        recommendation_type=recommendation_in.recommendation_type,
        recommendation_data=recommendation_in.recommendation_data,
        explanation=recommendation_in.explanation,
        campaign_id=campaign_id,
        is_applied=False
    )
    db.add(recommendation)
    db.commit()
    db.refresh(recommendation)
    
    return recommendation


@router.put("/{campaign_id}/recommendations/{recommendation_id}", response_model=schemas.Recommendation)
def update_recommendation(
    recommendation_in: schemas.RecommendationUpdate,
    campaign_id: int = Path(..., title="معرف الحملة"),
    recommendation_id: int = Path(..., title="معرف التوصية"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    تحديث توصية الحملة
    """
    # التحقق من وجود الحملة
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id,
        Campaign.user_id == current_user.id
    ).first()
    
    if not campaign:
        raise HTTPException(status_code=404, detail="الحملة غير موجودة")
    
    # البحث عن التوصية
    recommendation = db.query(Recommendation).filter(
        Recommendation.id == recommendation_id,
        Recommendation.campaign_id == campaign_id
    ).first()
    
    if not recommendation:
        raise HTTPException(status_code=404, detail="التوصية غير موجودة")
    
    # تحديث البيانات
    if recommendation_in.is_applied is not None:
        recommendation.is_applied = recommendation_in.is_applied
    if recommendation_in.feedback is not None:
        recommendation.feedback = recommendation_in.feedback
    
    db.add(recommendation)
    db.commit()
    db.refresh(recommendation)
    
    return recommendation
