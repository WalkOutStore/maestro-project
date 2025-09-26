from sqlalchemy import Column, Integer, String, DateTime, JSON, Text, Float, Boolean, ForeignKey, Index
from sqlalchemy.sql import func

from app.database import Base


class KnowledgeRule(Base):
    """
    نموذج القواعد الرمزية في قاعدة المعرفة
    """
    __tablename__ = "knowledge_rules"
    __table_args__ = {"sqlite_autoincrement": True}

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
    __table_args__ = {"sqlite_autoincrement": True}

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
    __table_args__ = {"sqlite_autoincrement": True}

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
    __table_args__ = {"sqlite_autoincrement": True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    content_type = Column(String)  # text, image, video
    template_data = Column(Text)  # قالب المحتوى
    variables = Column(JSON)  # المتغيرات التي يمكن استبدالها في القالب
    performance_score = Column(Float, default=0.0)  # تقييم أداء القالب
    usage_count = Column(Integer, default=0)  # عدد مرات استخدام القالب
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class APIUsage(Base):
    """
    نموذج لتتبع استخدام APIs الخارجية
    """
    __tablename__ = "api_usage"
    __table_args__ = {"sqlite_autoincrement": True}

    id = Column(Integer, primary_key=True, index=True)
    api_name = Column(String, index=True)  # google_trends, twitter, gemini
    endpoint = Column(String)  # الـ endpoint المستخدم
    request_data = Column(JSON)  # بيانات الطلب
    response_data = Column(JSON)  # بيانات الاستجابة
    success = Column(Boolean, default=True)  # نجاح أم فشل
    response_time = Column(Float)  # زمن الاستجابة بالثواني
    error_message = Column(Text)  # رسالة الخطأ إذا حدث
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class FeedbackAnalysis(Base):
    """
    نموذج لتحليل التغذية الراجعة من المستخدمين
    """
    __tablename__ = "feedback_analysis"
    __table_args__ = {"sqlite_autoincrement": True}

    id = Column(Integer, primary_key=True, index=True)
    feedback_type = Column(String, index=True)  # recommendation, content, campaign
    entity_id = Column(Integer)  # ID الكيان المرتبط بالتغذية الراجعة
    user_rating = Column(Integer)  # تقييم المستخدم (1-5)
    user_feedback = Column(Text)  # تعليق المستخدم
    system_analysis = Column(JSON)  # تحليل النظام للتغذية الراجعة
    improvement_suggestions = Column(JSON)  # اقتراحات للتحسين
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class CampaignPerformance(Base):
    """
    نموذج لتتبع أداء الحملات التسويقية
    """
    __tablename__ = "campaign_performance"
    __table_args__ = {"sqlite_autoincrement": True}

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), index=True)
    metric_name = Column(String, index=True)  # ctr, roi, impressions, clicks
    metric_value = Column(Float)  # قيمة المقياس
    metric_date = Column(DateTime(timezone=True))  # تاريخ القياس
    source = Column(String)  # مصدر البيانات (api, manual, calculated)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
