from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class KnowledgeRuleBase(BaseModel):
    """
    المخطط الأساسي للقاعدة المعرفية
    """
    name: str
    description: Optional[str] = None
    rule_type: str
    conditions: Dict[str, Any]
    actions: Dict[str, Any]
    priority: int = 0
    is_active: bool = True


class KnowledgeRuleCreate(KnowledgeRuleBase):
    """
    مخطط إنشاء قاعدة معرفية جديدة
    """
    pass


class KnowledgeRuleUpdate(BaseModel):
    """
    مخطط تحديث القاعدة المعرفية
    """
    name: Optional[str] = None
    description: Optional[str] = None
    conditions: Optional[Dict[str, Any]] = None
    actions: Optional[Dict[str, Any]] = None
    priority: Optional[int] = None
    is_active: Optional[bool] = None


class KnowledgeRule(KnowledgeRuleBase):
    """
    مخطط القاعدة المعرفية للعرض
    """
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class MLModelBase(BaseModel):
    """
    المخطط الأساسي لنموذج التعلم الآلي
    """
    name: str
    description: Optional[str] = None
    model_type: str
    model_path: str
    features: List[str]
    performance_metrics: Dict[str, float]
    version: str
    is_active: bool = True


class MLModelCreate(MLModelBase):
    """
    مخطط إنشاء نموذج تعلم آلي جديد
    """
    pass


class MLModelUpdate(BaseModel):
    """
    مخطط تحديث نموذج التعلم الآلي
    """
    name: Optional[str] = None
    description: Optional[str] = None
    model_path: Optional[str] = None
    features: Optional[List[str]] = None
    performance_metrics: Optional[Dict[str, float]] = None
    version: Optional[str] = None
    is_active: Optional[bool] = None


class MLModel(MLModelBase):
    """
    مخطط نموذج التعلم الآلي للعرض
    """
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class TrendDataBase(BaseModel):
    """
    المخطط الأساسي لبيانات الاتجاهات
    """
    keyword: str
    trend_source: str
    trend_value: float
    trend_data: Dict[str, Any]


class TrendDataCreate(TrendDataBase):
    """
    مخطط إنشاء بيانات اتجاهات جديدة
    """
    pass


class TrendData(TrendDataBase):
    """
    مخطط بيانات الاتجاهات للعرض
    """
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True


class ContentTemplateBase(BaseModel):
    """
    المخطط الأساسي لقالب المحتوى
    """
    name: str
    description: Optional[str] = None
    content_type: str
    template_data: str
    variables: Dict[str, str]
    performance_score: float = 0.0


class ContentTemplateCreate(ContentTemplateBase):
    """
    مخطط إنشاء قالب محتوى جديد
    """
    pass


class ContentTemplateUpdate(BaseModel):
    """
    مخطط تحديث قالب المحتوى
    """
    name: Optional[str] = None
    description: Optional[str] = None
    template_data: Optional[str] = None
    variables: Optional[Dict[str, str]] = None
    performance_score: Optional[float] = None


class ContentTemplate(ContentTemplateBase):
    """
    مخطط قالب المحتوى للعرض
    """
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
