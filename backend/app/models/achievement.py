from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base


class Achievement(Base):
    """
    نموذج الإنجازات في قاعدة البيانات
    """
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    icon = Column(String(200))  # URL or path to achievement icon
    points = Column(Integer, default=0)
    category = Column(String(50), default="general")  # e.g., "campaign", "learning", "social"
    rarity = Column(String(20), default="common")  # common, rare, epic, legendary
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship to track user achievements
    user_achievements = relationship("UserAchievement", back_populates="achievement")


class UserAchievement(Base):
    """
    نموذج ربط المستخدمين بالإنجازات المفتوحة
    """
    __tablename__ = "user_achievements"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    achievement_id = Column(Integer, ForeignKey("achievements.id"), nullable=False)
    unlocked_at = Column(DateTime(timezone=True), server_default=func.now())
    progress = Column(Integer, default=100)  # Progress percentage (0-100)
    is_completed = Column(Boolean, default=True)

    # Relationships
    user = relationship("User", back_populates="achievements")
    achievement = relationship("Achievement", back_populates="user_achievements")
