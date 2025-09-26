from sqlalchemy import Boolean, Column, Integer, String, Float, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Campaign(Base):
    """
    نموذج الحملة التسويقية في قاعدة البيانات
    """
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    product_name = Column(String)
    industry = Column(String)
    goal = Column(String) # Add the 'goal' column to the Campaign model.

    description = Column(Text)
    status = Column(String, default="draft")  # draft, active, paused, completed
    budget = Column(Float, default=0.0)
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    target_audience = Column(JSON)  # تخزين معلومات الجمهور المستهدف كـ JSON
    channels = Column(JSON)  # تخزين قنوات التسويق كـ JSON
    metrics = Column(JSON)  # تخزين مقاييس الأداء كـ JSON
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # العلاقة مع المستخدم
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", backref="campaigns")
    
    # العلاقة مع المحتوى
    contents = relationship("Content", back_populates="campaign")
    
    # العلاقة مع التوصيات
    recommendations = relationship("Recommendation", back_populates="campaign")


class Content(Base):
    """
    نموذج محتوى الحملة التسويقية في قاعدة البيانات
    """
    __tablename__ = "contents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content_type = Column(String)  # text, image, video
    content_data = Column(Text)  # محتوى النص أو رابط الصورة/الفيديو
    channel = Column(String)  # القناة التي سيتم نشر المحتوى عليها
    status = Column(String, default="draft")  # draft, published, archived
    performance = Column(JSON)  # تخزين بيانات أداء المحتوى كـ JSON
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # العلاقة مع الحملة
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))
    campaign = relationship("Campaign", back_populates="contents")


class Recommendation(Base):
    """
    نموذج توصيات الذكاء الاصطناعي في قاعدة البيانات
    """
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    recommendation_type = Column(String)  # content, channel, budget, audience
    recommendation_data = Column(JSON)  # بيانات التوصية
    explanation = Column(Text)  # شرح سبب التوصية (للشفافية)
    is_applied = Column(Boolean, default=False)  # هل تم تطبيق التوصية
    feedback = Column(Integer)  # تقييم المستخدم للتوصية (1-5)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # العلاقة مع الحملة
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))
    campaign = relationship("Campaign", back_populates="recommendations")