from sqlalchemy import Column, Integer, String, DateTime, JSON, Text, Float, Boolean
from sqlalchemy.sql import func

from app.database import Base


class KnowledgeRule(Base):
    """
    نموذج القواعد الرمزية في قاعدة المعرفة
    """
    __tablename__ = "knowledge_rules"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    rule_type = Column(String)  # channel, content, audience, budget
    conditions = Column(JSON)  # شروط تطبيق القاعدة
    actions = Column(JSON)  # الإجراءات التي يجب اتخاذها عند تحقق الشروط
    priority = Column(Integer, default=0)  # أولوية القاعدة
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class MLModel(Base):
    """
    نموذج لتخزين معلومات نماذج التعلم الآلي
    """
    __tablename__ = "ml_models"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    model_type = Column(String)  # ctr_prediction, roi_prediction, content_recommendation
    model_path = Column(String)  # مسار ملف النموذج
    features = Column(JSON)  # الميزات التي يستخدمها النموذج
    performance_metrics = Column(JSON)  # مقاييس أداء النموذج
    version = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class TrendData(Base):
    """
    نموذج لتخزين بيانات الاتجاهات
    """
    __tablename__ = "trend_data"

    id = Column(Integer, primary_key=True, index=True)
    keyword = Column(String, index=True)
    trend_source = Column(String)  # google_trends, twitter
    trend_value = Column(Float)  # قيمة الاتجاه
    trend_data = Column(JSON)  # بيانات إضافية عن الاتجاه
    timestamp = Column(DateTime(timezone=True), server_default=func.now())


class ContentTemplate(Base):
    """
    نموذج لتخزين قوالب المحتوى
    """
    __tablename__ = "content_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    content_type = Column(String)  # text, image, video
    template_data = Column(Text)  # قالب المحتوى
    variables = Column(JSON)  # المتغيرات التي يمكن استبدالها في القالب
    performance_score = Column(Float, default=0.0)  # تقييم أداء القالب
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
