from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Union
from datetime import datetime


class ContentBase(BaseModel):
    """
    المخطط الأساسي للمحتوى
    """
    title: str
    content_type: str
    content_data: str
    channel: str
    status: str = "draft"


class ContentCreate(ContentBase):
    """
    مخطط إنشاء محتوى جديد
    """
    campaign_id: int


class ContentUpdate(BaseModel):
    """
    مخطط تحديث المحتوى
    """
    title: Optional[str] = None
    content_type: Optional[str] = None
    content_data: Optional[str] = None
    channel: Optional[str] = None
    status: Optional[str] = None
    performance: Optional[Dict[str, Any]] = None


class Content(ContentBase):
    """
    مخطط المحتوى للعرض
    """
    id: int
    campaign_id: int
    performance: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class RecommendationBase(BaseModel):
    """
    المخطط الأساسي للتوصية
    """
    recommendation_type: str
    recommendation_data: Dict[str, Any]
    explanation: str


class RecommendationCreate(RecommendationBase):
    """
    مخطط إنشاء توصية جديدة
    """
    campaign_id: int


class RecommendationUpdate(BaseModel):
    """
    مخطط تحديث التوصية
    """
    is_applied: Optional[bool] = None
    feedback: Optional[int] = Field(None, ge=1, le=5)


class Recommendation(RecommendationBase):
    """
    مخطط التوصية للعرض
    """
    id: int
    campaign_id: int
    is_applied: bool
    feedback: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


class CampaignBase(BaseModel):
    """
    المخطط الأساسي للحملة التسويقية
    """
    name: str
    description: Optional[str] = None
    status: str = "draft"
    budget: float = 0.0
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    target_audience: Optional[Dict[str, Any]] = None
    channels: Optional[List[str]] = None


class CampaignCreate(CampaignBase):
    """
    مخطط إنشاء حملة تسويقية جديدة
    """
    pass


class CampaignUpdate(BaseModel):
    """
    مخطط تحديث الحملة التسويقية
    """
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    budget: Optional[float] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    target_audience: Optional[Dict[str, Any]] = None
    channels: Optional[List[str]] = None
    metrics: Optional[Dict[str, Any]] = None


class Campaign(CampaignBase):
    """
    مخطط الحملة التسويقية للعرض
    """
    id: int
    user_id: int
    metrics: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    contents: List[Content] = []
    recommendations: List[Recommendation] = []

    class Config:
        from_attributes = True


class CampaignWithDetails(Campaign):
    """
    مخطط الحملة التسويقية مع التفاصيل الكاملة
    """
    contents: List[Content]
    recommendations: List[Recommendation]
