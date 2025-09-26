from typing import List, Optional
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload

from app.models import Achievement, UserAchievement, User
from app.database import get_db

# ============================
# إنشاء Router
# ============================
router = APIRouter()

# ============================
# مسار الحصول على الإنجازات المفتوحة للمستخدم
# ============================
@router.get("/unlocked")
def get_unlocked_achievements(
    user_id: Optional[int] = Query(None, description="معرف المستخدم"),
    category: Optional[str] = Query(None, description="تصنيف الإنجاز"),
    db: Session = Depends(get_db)
):
    """
    الحصول على الإنجازات المفتوحة للمستخدم
    """
    query = db.query(UserAchievement).options(
        joinedload(UserAchievement.achievement)
    ).filter(UserAchievement.is_completed == True)

    if user_id:
        query = query.filter(UserAchievement.user_id == user_id)

    if category:
        query = query.join(Achievement).filter(Achievement.category == category)

    user_achievements = query.all()

    result = []
    for user_achievement in user_achievements:
        achievement_data = {
            "id": user_achievement.achievement.id,
            "name": user_achievement.achievement.name,
            "description": user_achievement.achievement.description,
            "icon": user_achievement.achievement.icon,
            "points": user_achievement.achievement.points,
            "category": user_achievement.achievement.category,
            "rarity": user_achievement.achievement.rarity,
            "unlocked_at": user_achievement.unlocked_at.isoformat() if user_achievement.unlocked_at else None,
            "progress": user_achievement.progress
        }
        result.append(achievement_data)

    return {
        "achievements": result,
        "total": len(result)
    }

# ============================
# مسار الحصول على تقدم الإنجازات للمستخدم
# ============================
@router.get("/progress")
def get_achievement_progress(
    user_id: Optional[int] = Query(None, description="معرف المستخدم"),
    category: Optional[str] = Query(None, description="تصنيف الإنجاز"),
    include_completed: bool = Query(True, description="تضمين الإنجازات المكتملة"),
    db: Session = Depends(get_db)
):
    """
    الحصول على تقدم الإنجازات للمستخدم
    """
    query = db.query(UserAchievement).options(
        joinedload(UserAchievement.achievement)
    )

    if user_id:
        query = query.filter(UserAchievement.user_id == user_id)

    if category:
        query = query.join(Achievement).filter(Achievement.category == category)

    if not include_completed:
        query = query.filter(UserAchievement.is_completed == False)

    user_achievements = query.all()

    result = []
    for user_achievement in user_achievements:
        achievement_data = {
            "achievement_id": user_achievement.achievement.id,
            "name": user_achievement.achievement.name,
            "description": user_achievement.achievement.description,
            "icon": user_achievement.achievement.icon,
            "points": user_achievement.achievement.points,
            "category": user_achievement.achievement.category,
            "rarity": user_achievement.achievement.rarity,
            "progress": user_achievement.progress,
            "is_completed": user_achievement.is_completed,
            "unlocked_at": user_achievement.unlocked_at.isoformat() if user_achievement.unlocked_at else None,
            "last_updated": user_achievement.achievement.updated_at.isoformat() if user_achievement.achievement.updated_at else None
        }
        result.append(achievement_data)

    return {
        "achievements": result,
        "total": len(result)
    }

# ============================
# مسار فتح إنجاز جديد للمستخدم
# ============================
@router.post("/unlock")
def unlock_achievement(
    user_id: int,
    achievement_id: int,
    progress: int = 100,
    db: Session = Depends(get_db)
):
    """
    فتح إنجاز جديد للمستخدم
    """
    # التحقق من وجود المستخدم
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="المستخدم غير موجود")

    # التحقق من وجود الإنجاز
    achievement = db.query(Achievement).filter(Achievement.id == achievement_id).first()
    if not achievement:
        raise HTTPException(status_code=404, detail="الإنجاز غير موجود")

    # التحقق من عدم وجود الإنجاز مسبقاً
    existing = db.query(UserAchievement).filter(
        UserAchievement.user_id == user_id,
        UserAchievement.achievement_id == achievement_id
    ).first()

    if existing:
        # تحديث التقدم إذا كان الإنجاز موجود مسبقاً
        existing.progress = progress
        existing.is_completed = progress >= 100
        if existing.is_completed and not existing.unlocked_at:
            existing.unlocked_at = datetime.utcnow()
        db.commit()
        db.refresh(existing)
        return {"message": "تم تحديث الإنجاز", "achievement": existing}

    # إنشاء إنجاز جديد للمستخدم
    user_achievement = UserAchievement(
        user_id=user_id,
        achievement_id=achievement_id,
        progress=progress,
        is_completed=progress >= 100
    )

    if user_achievement.is_completed:
        user_achievement.unlocked_at = datetime.utcnow()

    db.add(user_achievement)
    db.commit()
    db.refresh(user_achievement)

    return {"message": "تم فتح الإنجاز بنجاح", "achievement": user_achievement}

# ============================
# مسار الحصول على جميع الإنجازات المتاحة
# ============================
@router.get("/available")
def get_available_achievements(
    category: Optional[str] = Query(None, description="تصنيف الإنجاز"),
    rarity: Optional[str] = Query(None, description="ندرة الإنجاز"),
    db: Session = Depends(get_db)
):
    """
    الحصول على جميع الإنجازات المتاحة
    """
    query = db.query(Achievement).filter(Achievement.is_active == True)

    if category:
        query = query.filter(Achievement.category == category)

    if rarity:
        query = query.filter(Achievement.rarity == rarity)

    achievements = query.all()

    result = []
    for achievement in achievements:
        achievement_data = {
            "id": achievement.id,
            "name": achievement.name,
            "description": achievement.description,
            "icon": achievement.icon,
            "points": achievement.points,
            "category": achievement.category,
            "rarity": achievement.rarity,
            "created_at": achievement.created_at.isoformat() if achievement.created_at else None
        }
        result.append(achievement_data)

    return {
        "achievements": result,
        "total": len(result)
    }
