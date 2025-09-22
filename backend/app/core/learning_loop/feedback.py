from typing import Dict, Any, List, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from app.models.campaign import Recommendation


class FeedbackProcessor:
    """
    معالج التغذية الراجعة الذي يجمع ويحلل تفاعلات المستخدم
    """
    
    def __init__(self, db: Session = None):
        """
        تهيئة معالج التغذية الراجعة
        """
        self.db = db
    
    def save_recommendation_feedback(self, recommendation_id: int, feedback_data: Dict[str, Any]) -> bool:
        """
        حفظ التغذية الراجعة على توصية
        """
        if self.db:
            recommendation = self.db.query(Recommendation).filter(Recommendation.id == recommendation_id).first()
            if recommendation:
                # تحديث حالة التطبيق
                if "is_applied" in feedback_data:
                    recommendation.is_applied = feedback_data["is_applied"]
                
                # تحديث تقييم التوصية
                if "rating" in feedback_data:
                    recommendation.feedback = feedback_data["rating"]
                
                self.db.commit()
                return True
        
        return False
    
    def get_recommendation_feedback_stats(self, campaign_id: Optional[int] = None) -> Dict[str, Any]:
        """
        الحصول على إحصائيات التغذية الراجعة للتوصيات
        """
        stats = {
            "total_recommendations": 0,
            "applied_recommendations": 0,
            "feedback_received": 0,
            "average_rating": 0,
            "by_type": {}
        }
        
        if self.db:
            # إنشاء استعلام قاعدة البيانات
            query = self.db.query(Recommendation)
            if campaign_id:
                query = query.filter(Recommendation.campaign_id == campaign_id)
            
            recommendations = query.all()
            
            # حساب الإحصائيات
            stats["total_recommendations"] = len(recommendations)
            
            applied_count = 0
            feedback_count = 0
            total_rating = 0
            type_stats = {}
            
            for rec in recommendations:
                # حساب التوصيات المطبقة
                if rec.is_applied:
                    applied_count += 1
                
                # حساب التغذية الراجعة
                if rec.feedback:
                    feedback_count += 1
                    total_rating += rec.feedback
                
                # حساب الإحصائيات حسب النوع
                rec_type = rec.recommendation_type
                if rec_type not in type_stats:
                    type_stats[rec_type] = {
                        "total": 0,
                        "applied": 0,
                        "feedback_received": 0,
                        "average_rating": 0
                    }
                
                type_stats[rec_type]["total"] += 1
                
                if rec.is_applied:
                    type_stats[rec_type]["applied"] += 1
                
                if rec.feedback:
                    type_stats[rec_type]["feedback_received"] += 1
                    type_stats[rec_type]["average_rating"] += rec.feedback
            
            # حساب المتوسطات
            stats["applied_recommendations"] = applied_count
            stats["feedback_received"] = feedback_count
            stats["average_rating"] = total_rating / feedback_count if feedback_count > 0 else 0
            
            # حساب المتوسطات حسب النوع
            for rec_type, type_data in type_stats.items():
                if type_data["feedback_received"] > 0:
                    type_data["average_rating"] = type_data["average_rating"] / type_data["feedback_received"]
            
            stats["by_type"] = type_stats
        
        return stats
    
    def collect_user_interactions(self, user_id: int, interaction_data: Dict[str, Any]) -> bool:
        """
        جمع تفاعلات المستخدم مع النظام
        """
        # هذه الدالة يمكن أن تخزن تفاعلات المستخدم في قاعدة البيانات
        # مثل النقرات، والوقت المستغرق، والصفحات المزارة، إلخ.
        # يمكن استخدام هذه البيانات لاحقًا لتحسين النماذج
        
        # هذا مثال بسيط، يمكن توسيعه حسب احتياجات المشروع
        
        # نعيد True للإشارة إلى نجاح العملية
        return True
    
    def analyze_feedback_trends(self, days: int = 30) -> Dict[str, Any]:
        """
        تحليل اتجاهات التغذية الراجعة على مدار فترة زمنية
        """
        # هذه الدالة يمكن أن تحلل اتجاهات التغذية الراجعة على مدار فترة زمنية
        # مثل تغير متوسط التقييم، ونسبة التوصيات المطبقة، إلخ.
        
        # هذا مثال بسيط، يمكن توسيعه حسب احتياجات المشروع
        
        # نعيد بيانات افتراضية
        return {
            "rating_trend": [
                {"date": "2023-01-01", "average_rating": 4.2},
                {"date": "2023-01-08", "average_rating": 4.3},
                {"date": "2023-01-15", "average_rating": 4.4},
                {"date": "2023-01-22", "average_rating": 4.5},
                {"date": "2023-01-29", "average_rating": 4.6}
            ],
            "application_rate_trend": [
                {"date": "2023-01-01", "application_rate": 0.65},
                {"date": "2023-01-08", "application_rate": 0.68},
                {"date": "2023-01-15", "application_rate": 0.70},
                {"date": "2023-01-22", "application_rate": 0.72},
                {"date": "2023-01-29", "application_rate": 0.75}
            ]
        }
    
    def get_feedback_for_model_update(self, model_type: str, limit: int = 100) -> List[Dict[str, Any]]:
        """
        الحصول على التغذية الراجعة لتحديث نموذج معين
        """
        feedback_data = []
        
        if self.db:
            # استعلام قاعدة البيانات للحصول على التوصيات ذات التغذية الراجعة
            recommendations = self.db.query(Recommendation).filter(
                Recommendation.recommendation_type == model_type,
                Recommendation.feedback.isnot(None)
            ).order_by(Recommendation.created_at.desc()).limit(limit).all()
            
            for rec in recommendations:
                # استخراج البيانات المفيدة للتحديث
                feedback_data.append({
                    "recommendation_id": rec.id,
                    "recommendation_data": rec.recommendation_data,
                    "is_applied": rec.is_applied,
                    "rating": rec.feedback,
                    "created_at": rec.created_at.isoformat()
                })
        
        return feedback_data
