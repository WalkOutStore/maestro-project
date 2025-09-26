from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.models.campaign import Recommendation

class FeedbackProcessor:
    """
    معالج التغذية الراجعة بدون أي بيانات افتراضية.
    يعتمد فقط على البيانات الفعلية في قاعدة البيانات.
    """

    def __init__(self, db: Session = None):
        self.db = db

    def save_recommendation_feedback(self, recommendation_id: int, feedback_data: Dict[str, Any]) -> bool:
        """
        حفظ التغذية الراجعة على توصية معينة
        """
        if self.db:
            recommendation = self.db.query(Recommendation).filter(Recommendation.id == recommendation_id).first()
            if recommendation:
                if "is_applied" in feedback_data:
                    recommendation.is_applied = feedback_data["is_applied"]
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
            query = self.db.query(Recommendation)
            if campaign_id:
                query = query.filter(Recommendation.campaign_id == campaign_id)
            recommendations = query.all()

            stats["total_recommendations"] = len(recommendations)

            applied_count = 0
            feedback_count = 0
            total_rating = 0
            type_stats = {}

            for rec in recommendations:
                if rec.is_applied:
                    applied_count += 1
                if rec.feedback:
                    feedback_count += 1
                    total_rating += rec.feedback

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

            stats["applied_recommendations"] = applied_count
            stats["feedback_received"] = feedback_count
            stats["average_rating"] = total_rating / feedback_count if feedback_count > 0 else 0

            for rec_type, type_data in type_stats.items():
                if type_data["feedback_received"] > 0:
                    type_data["average_rating"] = type_data["average_rating"] / type_data["feedback_received"]

            stats["by_type"] = type_stats

        return stats

    def collect_user_interactions(self, user_id: int, interaction_data: Dict[str, Any]) -> bool:
        """
        جمع تفاعلات المستخدم مع النظام (يمكن تخزينها لاحقًا في DB)
        """
        return True

    def analyze_feedback_trends(self, days: int = 30) -> Dict[str, Any]:
        """
        تحليل اتجاهات التغذية الراجعة على مدار فترة زمنية
        بدون أي بيانات افتراضية
        """
        trends = {
            "rating_trend": [],
            "application_rate_trend": [],
            "total_feedback": 0,
            "average_rating": 0,
            "application_rate": 0
        }

        if self.db:
            start_date = datetime.now() - timedelta(days=days)
            recommendations = self.db.query(Recommendation).filter(
                Recommendation.created_at >= start_date
            ).all()

            if recommendations:
                weekly_data = {}
                for rec in recommendations:
                    week_start = rec.created_at.replace(hour=0, minute=0, second=0, microsecond=0)
                    week_key = week_start.strftime("%Y-%m-%d")

                    if week_key not in weekly_data:
                        weekly_data[week_key] = {
                            "total_recommendations": 0,
                            "applied_recommendations": 0,
                            "total_rating": 0,
                            "rated_recommendations": 0
                        }

                    weekly_data[week_key]["total_recommendations"] += 1
                    if rec.is_applied:
                        weekly_data[week_key]["applied_recommendations"] += 1
                    if rec.feedback:
                        weekly_data[week_key]["total_rating"] += rec.feedback
                        weekly_data[week_key]["rated_recommendations"] += 1

                for week_key, data in sorted(weekly_data.items()):
                    avg_rating = data["total_rating"] / data["rated_recommendations"] if data["rated_recommendations"] > 0 else 0
                    app_rate = data["applied_recommendations"] / data["total_recommendations"] if data["total_recommendations"] > 0 else 0
                    trends["rating_trend"].append({
                        "date": week_key,
                        "average_rating": round(avg_rating, 2)
                    })
                    trends["application_rate_trend"].append({
                        "date": week_key,
                        "application_rate": round(app_rate, 2)
                    })

                total_rating = sum(rec.feedback for rec in recommendations if rec.feedback)
                rated_count = sum(1 for rec in recommendations if rec.feedback)
                applied_count = sum(1 for rec in recommendations if rec.is_applied)

                trends["total_feedback"] = len(recommendations)
                trends["average_rating"] = round(total_rating / rated_count, 2) if rated_count > 0 else 0
                trends["application_rate"] = round(applied_count / len(recommendations), 2) if recommendations else 0

        return trends

    def get_feedback_for_model_update(self, model_type: str, limit: int = 100) -> List[Dict[str, Any]]:
        """
        الحصول على التغذية الراجعة لتحديث نموذج معين
        """
        feedback_data = []

        if self.db:
            recommendations = self.db.query(Recommendation).filter(
                Recommendation.recommendation_type == model_type,
                Recommendation.feedback.isnot(None)
            ).order_by(Recommendation.created_at.desc()).limit(limit).all()

            for rec in recommendations:
                feedback_data.append({
                    "recommendation_id": rec.id,
                    "recommendation_data": rec.recommendation_data,
                    "is_applied": rec.is_applied,
                    "rating": rec.feedback,
                    "created_at": rec.created_at.isoformat()
                })

        return feedback_data