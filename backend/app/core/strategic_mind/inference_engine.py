from typing import Dict, Any, List, Optional, Tuple
import numpy as np
import pandas as pd
import joblib
import os
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.strategic_mind.knowledge_base import DynamicKnowledgeBase
from app.models.knowledge_base import MLModel
from app.config import settings
from .ml_manager import ml_manager


class HybridInferenceEngine:
    """
    محرك الاستدلال الهجين الذي يجمع بين القواعد الرمزية ونماذج التعلم الآلي
    """
    
    def __init__(self, db: Session = None):
        """
        تهيئة محرك الاستدلال
        """
        self.db = db
        self.knowledge_base = DynamicKnowledgeBase(db)
        self.ml_models = {}
        self._load_ml_models()
    
    def _load_ml_models(self) -> None:
        """
        تحميل نماذج التعلم الآلي من قاعدة البيانات
        """
        if self.db:
            models = self.db.query(MLModel).filter(MLModel.is_active == True).all()
            for model in models:
                model_path = model.model_path
                if os.path.exists(model_path):
                    try:
                        self.ml_models[model.model_type] = {
                            "model": joblib.load(model_path),
                            "features": model.features,
                            "metadata": {
                                "name": model.name,
                                "version": model.version,
                                "performance": model.performance_metrics
                            }
                        }
                    except Exception as e:
                        print(f"Error loading model {model.name}: {e}")
    
    def predict_ctr(self, campaign_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        التنبؤ بمعدل النقر إلى الظهور (CTR) باستخدام نماذج التعلم الآلي
        """
        try:
            print(f"🔍 DEBUG: predict_ctr called with data: {campaign_data}")

            # استخدام قاعدة المعرفة أولاً للتحقق من القواعد
            rules_result = self.knowledge_base.evaluate_rules(campaign_data, "ctr_prediction")
            print(f"🔍 DEBUG: rules_result: {rules_result}")

            # إذا كانت هناك قواعد تنطبق، استخدمها
            if rules_result:
                ctr_values = []
                for action in rules_result:
                    if "actions" in action and "ctr" in action["actions"]:
                        ctr_values.append(action["actions"]["ctr"])
                if ctr_values:
                    ctr_value = sum(ctr_values) / len(ctr_values)
                    print(f"✅ DEBUG: using knowledge rules, ctr_value: {ctr_value}")
                    return {
                        "prediction": ctr_value if ctr_value is not None else 0.05,
                        "confidence": 0.9,
                        "method": "knowledge_rules",
                        "explanation": "تم استخدام قواعد المعرفة للتنبؤ",
                        "factors": [
                            {"name": "الصناعة", "value": 0.3},
                            {"name": "الميزانية", "value": 0.25},
                            {"name": "القناة", "value": 0.2},
                            {"name": "الفئة العمرية", "value": 0.15},
                            {"name": "نوع المحتوى", "value": 0.1}
                        ],
                        "trend": [
                            {"name": "الأسبوع 1", "value": 0.06},
                            {"name": "الأسبوع 2", "value": 0.08},
                            {"name": "الأسبوع 3", "value": 0.07},
                            {"name": "الأسبوع 4", "value": 0.09}
                        ],
                        "benchmark": 0.05
                    }

            print("🔍 DEBUG: no rules matched, using fallback logic")
            # استخدام نماذج التعلم الآلي
            features = self._extract_ctr_features(campaign_data)

            # استخدام نموذج CTR إذا كان متوفراً
            ctr_model = self.ml_models.get("ctr")
            if ctr_model:
                prediction = ctr_model["model"].predict([features])[0]
                confidence = ctr_model["metadata"]["performance"].get("r2_score", 0.7)

                return {
                    "prediction": max(0, min(1, prediction)),  # التأكد من أن القيمة بين 0 و 1
                    "confidence": confidence,
                    "method": "ml_model",
                    "explanation": f"تم استخدام نموذج {ctr_model['metadata']['name']} للتنبؤ"
                }

            # تنبؤ افتراضي بسيط بناءً على البيانات
            base_ctr = 0.05  # CTR أساسي 5%

            # تعديل بناءً على الصناعة
            industry_multipliers = {
                "technology": 1.2,
                "fashion": 1.1,
                "food": 0.9,
                "automotive": 0.8,
                "healthcare": 0.7
            }

            industry = campaign_data.get("industry", "technology").lower()
            multiplier = industry_multipliers.get(industry, 1.0)

            # تعديل بناءً على الميزانية
            budget = campaign_data.get("budget", 1000)
            budget_multiplier = min(1.5, budget / 1000)

            # تعديل بناءً على القناة
            channel_multipliers = {
                "social_media": 1.0,
                "search": 1.3,
                "display": 0.8,
                "video": 1.1,
                "email": 0.9
            }

            channel = campaign_data.get("channel", "social_media").lower()
            channel_multiplier = channel_multipliers.get(channel, 1.0)

            prediction = base_ctr * multiplier * budget_multiplier * channel_multiplier

            return {
                "prediction": max(0.01, min(0.5, prediction)),
                "confidence": 0.6,
                "method": "heuristic",
                "explanation": f"تنبؤ بناءً على: الصناعة ({multiplier}x), الميزانية ({budget_multiplier:.1f}x), القناة ({channel_multiplier}x)",
                "factors": [
                    {"name": "الصناعة", "value": multiplier / 3.0},
                    {"name": "الميزانية", "value": budget_multiplier / 3.0},
                    {"name": "القناة", "value": channel_multiplier / 3.0},
                    {"name": "الفئة العمرية", "value": 0.15},
                    {"name": "نوع المحتوى", "value": 0.1}
                ],
                "trend": [
                    {"name": "الأسبوع 1", "value": prediction * 0.8},
                    {"name": "الأسبوع 2", "value": prediction * 0.9},
                    {"name": "الأسبوع 3", "value": prediction * 1.1},
                    {"name": "الأسبوع 4", "value": prediction * 1.2}
                ],
                "benchmark": 0.05
            }

        except Exception as e:
            print(f"Error in CTR prediction: {e}")
            return {
                "prediction": 0.05,
                "confidence": 0.3,
                "method": "fallback",
                "explanation": f"خطأ في التنبؤ: {str(e)}",
                "factors": [
                    {"name": "الصناعة", "value": 0.2},
                    {"name": "الميزانية", "value": 0.2},
                    {"name": "القناة", "value": 0.2},
                    {"name": "الفئة العمرية", "value": 0.2},
                    {"name": "نوع المحتوى", "value": 0.2}
                ],
                "trend": [
                    {"name": "الأسبوع 1", "value": 0.04},
                    {"name": "الأسبوع 2", "value": 0.05},
                    {"name": "الأسبوع 3", "value": 0.06},
                    {"name": "الأسبوع 4", "value": 0.05}
                ],
                "benchmark": 0.05
            }

    def predict_roi(self, campaign_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        التنبؤ بالعائد على الاستثمار (ROI) باستخدام نماذج التعلم الآلي
        """
        try:
            # استخدام قاعدة المعرفة أولاً
            rules_result = self.knowledge_base.evaluate_rules(campaign_data, "roi_prediction")

            if rules_result:
                roi_value = None
                for action in rules_result:
                    if "actions" in action and "roi" in action["actions"]:
                        roi_value = action["actions"]["roi"]
                        break
                return {
                    "prediction": roi_value if roi_value is not None else 2.0,
                    "confidence": 0.9,
                    "method": "knowledge_rules",
                    "explanation": "تم استخدام قواعد المعرفة للتنبؤ"
                }

            # استخدام نماذج التعلم الآلي
            features = self._extract_roi_features(campaign_data)

            roi_model = self.ml_models.get("roi")
            if roi_model:
                prediction = roi_model["model"].predict([features])[0]
                confidence = roi_model["metadata"]["performance"].get("r2_score", 0.7)

                return {
                    "prediction": max(0, prediction),
                    "confidence": confidence,
                    "method": "ml_model",
                    "explanation": f"تم استخدام نموذج {roi_model['metadata']['name']} للتنبؤ"
                }

            # تنبؤ افتراضي بسيط
            base_roi = 2.0  # ROI أساسي 200%

            # تعديل بناءً على الصناعة
            industry_multipliers = {
                "technology": 1.3,
                "fashion": 1.1,
                "food": 0.9,
                "automotive": 1.0,
                "healthcare": 0.8
            }

            industry = campaign_data.get("industry", "technology").lower()
            multiplier = industry_multipliers.get(industry, 1.0)

            # تعديل بناءً على الميزانية
            budget = campaign_data.get("budget", 1000)
            budget_multiplier = min(2.0, 1.0 + (budget / 5000))

            # تعديل بناءً على القناة
            channel_multipliers = {
                "social_media": 1.0,
                "search": 1.4,
                "display": 0.7,
                "video": 1.2,
                "email": 0.8
            }

            channel = campaign_data.get("channel", "social_media").lower()
            channel_multiplier = channel_multipliers.get(channel, 1.0)

            prediction = base_roi * multiplier * budget_multiplier * channel_multiplier

            return {
                "prediction": max(0.5, min(5.0, prediction)),
                "confidence": 0.6,
                "method": "heuristic",
                "explanation": f"تنبؤ بناءً على: الصناعة ({multiplier}x), الميزانية ({budget_multiplier:.1f}x), القناة ({channel_multiplier}x)"
            }

        except Exception as e:
            print(f"Error in ROI prediction: {e}")
            return {
                "prediction": 2.0,
                "confidence": 0.3,
                "method": "fallback",
                "explanation": f"خطأ في التنبؤ: {str(e)}"
            }

    def recommend_channels(self, campaign_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        توصية بقنوات التسويق المناسبة باستخدام نماذج التعلم الآلي
        """
        try:
            # Prepare context for rule evaluation
            context = campaign_data.copy()

            # Handle audience_age for rule evaluation
            if "audience_age" in context:
                age_range = context["audience_age"]
                if isinstance(age_range, str):
                    age_parts = age_range.split(',')
                    if len(age_parts) >= 2:
                        avg_age = (int(age_parts[0]) + int(age_parts[1])) / 2
                        context["audience_age_avg"] = avg_age
                    else:
                        context["audience_age_avg"] = int(age_parts[0]) if age_parts else 30
                elif isinstance(age_range, list):
                    context["audience_age_avg"] = (age_range[0] + age_range[1]) / 2 if len(age_range) >= 2 else 30

            # استخدام قاعدة المعرفة أولاً
            rules_result = self.knowledge_base.evaluate_rules(context, "channel_recommendation")

            if rules_result:
                recommended_channels = []
                for action in rules_result:
                    if "recommended_channels" in action.get("actions", {}):
                        recommended_channels.extend(action["actions"]["recommended_channels"])
                if recommended_channels:
                    return recommended_channels
                else:
                    # If no recommended channels are found in the rules, use the default logic
                    print("No recommended channels found in rules, using default logic")

            # استخدام نماذج التعلم الآلي
            features = self._extract_channel_features(campaign_data)

            # تنبؤ افتراضي بسيط
            channels = [
                {"channel": "social_media", "score": 0.85, "reason": "مناسب للفئة العمرية المستهدفة"},
                {"channel": "search", "score": 0.75, "reason": "فعال للمنتجات التقنية"},
                {"channel": "display", "score": 0.65, "reason": "تغطية واسعة للجمهور"},
                {"channel": "video", "score": 0.70, "reason": "محتوى تفاعلي جذاب"},
                {"channel": "email", "score": 0.55, "reason": "تكلفة منخفضة للتواصل المباشر"}
            ]

            # تعديل الدرجات بناءً على البيانات
            industry = campaign_data.get("industry", "technology").lower()
            budget = campaign_data.get("budget", 1000)

            if industry == "technology":
                channels[0]["score"] += 0.1  # زيادة درجة وسائل التواصل الاجتماعي
                channels[1]["score"] += 0.15  # زيادة درجة البحث

            if budget > 5000:
                channels[2]["score"] += 0.1  # زيادة درجة الإعلانات المصورة للميزانيات الكبيرة

            # ترتيب القنوات حسب الدرجة
            channels.sort(key=lambda x: x["score"], reverse=True)

            return channels

        except Exception as e:
            print(f"Error in channel recommendation: {e}")
            return [
                {"channel": "social_media", "score": 0.8, "reason": "قناة افتراضية", "confidence": 0.7},
                {"channel": "search", "score": 0.7, "reason": "قناة افتراضية", "confidence": 0.6}
            ]

    def _extract_ctr_features(self, campaign_data: Dict[str, Any]) -> List[float]:
        """
        استخراج الميزات لتنبؤ CTR
        """
        features = []

        # تحويل الصناعة إلى رقم
        industry_map = {"technology": 1, "fashion": 2, "food": 3, "automotive": 4, "healthcare": 5}
        industry = campaign_data.get("industry", "technology").lower()
        features.append(industry_map.get(industry, 1))

        # تحويل القناة إلى رقم
        channel_map = {"social_media": 1, "search": 2, "display": 3, "video": 4, "email": 5}
        channel = campaign_data.get("channel", "social_media").lower()
        features.append(channel_map.get(channel, 1))

        # الميزانية (طبيعية)
        budget = campaign_data.get("budget", 1000)
        features.append(budget / 10000)  # تطبيع

        # الفئة العمرية (متوسط)
        age_range = campaign_data.get("audience_age", [25, 45])
        if isinstance(age_range, str):
            # إذا كانت النطاق مفصولاً بفواصل، قسمه
            age_parts = age_range.split(',')
            if len(age_parts) >= 2:
                avg_age = (int(age_parts[0]) + int(age_parts[1])) / 2
            else:
                avg_age = int(age_parts[0]) if age_parts else 30
        elif isinstance(age_range, list):
            avg_age = (age_range[0] + age_range[1]) / 2 if len(age_range) >= 2 else 30
        else:
            avg_age = 30
        features.append(avg_age / 100)  # تطبيع

        return features

    def _extract_roi_features(self, campaign_data: Dict[str, Any]) -> List[float]:
        """
        استخراج الميزات لتنبؤ ROI
        """
        features = []

        # تحويل الصناعة إلى رقم
        industry_map = {"technology": 1, "fashion": 2, "food": 3, "automotive": 4, "healthcare": 5}
        industry = campaign_data.get("industry", "technology").lower()
        features.append(industry_map.get(industry, 1))

        # الميزانية
        budget = campaign_data.get("budget", 1000)
        features.append(budget / 10000)

        # المدة الزمنية
        duration = campaign_data.get("duration", 30)
        features.append(duration / 90)  # تطبيع على 90 يوم

        # نوع المحتوى
        content_type = campaign_data.get("content_type", "mixed")
        content_map = {"video": 1, "image": 2, "text": 3, "mixed": 4}
        features.append(content_map.get(content_type, 4))

        return features

    def _extract_channel_features(self, campaign_data: Dict[str, Any]) -> List[float]:
        """
        استخراج الميزات لتوصية القنوات
        """
        features = []

        # تحويل الصناعة إلى رقم
        industry_map = {"technology": 1, "fashion": 2, "food": 3, "automotive": 4, "healthcare": 5}
        industry = campaign_data.get("industry", "technology").lower()
        features.append(industry_map.get(industry, 1))

        # الميزانية
        budget = campaign_data.get("budget", 1000)
        features.append(budget / 10000)

        # الفئة العمرية
        age_range = campaign_data.get("audience_age", [25, 45])
        if isinstance(age_range, str):
            # إذا كانت النطاق مفصولاً بفواصل، قسمه
            age_parts = age_range.split(',')
            if len(age_parts) >= 2:
                avg_age = (int(age_parts[0]) + int(age_parts[1])) / 2
            else:
                avg_age = int(age_parts[0]) if age_parts else 30
        elif isinstance(age_range, list):
            avg_age = (age_range[0] + age_range[1]) / 2 if len(age_range) >= 2 else 30
        else:
            avg_age = 30
        features.append(avg_age / 100)

        # الهدف
        goal = campaign_data.get("goal", "awareness")
        goal_map = {"awareness": 1, "consideration": 2, "conversion": 3}
        features.append(goal_map.get(goal, 1))

        return features
    
    def _prepare_features(self, data: Dict[str, Any], required_features: List[str]) -> Optional[np.ndarray]:
        """
        تحضير ميزات البيانات للنموذج
        """
        try:
            # تحويل البيانات إلى DataFrame
            df = pd.DataFrame([data])
            
            # التحقق من وجود جميع الميزات المطلوبة
            missing_features = [f for f in required_features if f not in df.columns]
            if missing_features:
                print(f"Missing features: {missing_features}")
                return None
            
            # اختيار الميزات المطلوبة فقط
            X = df[required_features].values
            return X
        except Exception as e:
            print(f"Error preparing features: {e}")
            return None
    
    def _combine_predictions(self, rule_actions: List[Dict[str, Any]], ml_prediction: Optional[float]) -> float:
        """
        دمج التنبؤات من القواعد الرمزية ونموذج التعلم الآلي
        """
        # استخراج التنبؤات من القواعد الرمزية
        rule_predictions = []
        rule_weights = []
        
        for action in rule_actions:
            if "actions" in action and "prediction" in action["actions"]:
                rule_predictions.append(action["actions"]["prediction"])
                rule_weights.append(action["actions"].get("weight", 1.0))
        
        # إذا لم تكن هناك تنبؤات من القواعد الرمزية، استخدم تنبؤ نموذج التعلم الآلي فقط
        if not rule_predictions:
            return ml_prediction if ml_prediction is not None else 0.0
        
        # إذا لم يكن هناك تنبؤ من نموذج التعلم الآلي، استخدم متوسط التنبؤات من القواعد الرمزية
        if ml_prediction is None:
            if rule_weights:
                weighted_sum = sum(p * w for p, w in zip(rule_predictions, rule_weights))
                total_weight = sum(rule_weights)
                return weighted_sum / total_weight if total_weight > 0 else 0.0
            else:
                return sum(rule_predictions) / len(rule_predictions) if rule_predictions else 0.0
        
        # دمج التنبؤات من القواعد الرمزية ونموذج التعلم الآلي
        # هذا مثال بسيط، يمكن تنفيذ منطق أكثر تعقيدًا
        ml_weight = 0.7  # وزن نموذج التعلم الآلي
        rule_weight = 0.3  # وزن القواعد الرمزية
        
        if rule_weights:
            weighted_sum = sum(p * w for p, w in zip(rule_predictions, rule_weights))
            total_weight = sum(rule_weights)
            rule_prediction = weighted_sum / total_weight if total_weight > 0 else 0.0
        else:
            rule_prediction = sum(rule_predictions) / len(rule_predictions) if rule_predictions else 0.0
        
        return ml_weight * ml_prediction + rule_weight * rule_prediction
    
    def update_from_feedback(self, feedback_data: Dict[str, Any]) -> bool:
        """
        تحديث النماذج بناءً على التغذية الراجعة مع تتبع الأداء
        """
        try:
            # تحديث القواعد الرمزية
            if "rule_feedback" in feedback_data:
                for rule_feedback in feedback_data["rule_feedback"]:
                    rule_id = rule_feedback.get("rule_id")
                    if rule_id:
                        self.knowledge_base.update_from_feedback(rule_id, rule_feedback)

            # تحديث نماذج التعلم الآلي
            if "ml_feedback" in feedback_data:
                self._update_ml_models_from_feedback(feedback_data["ml_feedback"])

            # تتبع أداء النماذج
            self._track_model_performance(feedback_data)

            return True
        except Exception as e:
            print(f"Error updating from feedback: {e}")
            return False

    def _update_ml_models_from_feedback(self, ml_feedback: Dict[str, Any]) -> None:
        """
        تحديث نماذج التعلم الآلي بناءً على التغذية الراجعة
        """
        try:
            # هذه الوظيفة يمكن أن تقوم بإعادة تدريب النماذج أو تعديل معاملاتها
            # بناءً على التغذية الراجعة من المستخدمين

            print("🔄 Updating ML models from feedback...")

            # في التطبيق الحقيقي، يمكن:
            # 1. جمع المزيد من البيانات للتدريب
            # 2. تعديل معاملات النموذج
            # 3. إعادة تدريب النموذج ببيانات جديدة
            # 4. تحديث أوزان الميزات

            # مثال بسيط: تسجيل التغذية الراجعة للتحسين المستقبلي
            if "model_performance" in ml_feedback:
                performance = ml_feedback["model_performance"]
                print(f"📊 Model performance feedback: {performance}")

        except Exception as e:
            print(f"Error updating ML models: {e}")

    def _track_model_performance(self, feedback_data: Dict[str, Any]) -> None:
        """
        تتبع أداء النماذج وحفظ المقاييس
        """
        try:
            # حفظ مقاييس الأداء للتحليل المستقبلي
            performance_metrics = {
                "timestamp": datetime.now().isoformat(),
                "feedback_type": feedback_data.get("type", "general"),
                "user_satisfaction": feedback_data.get("satisfaction_score", 0),
                "model_accuracy": feedback_data.get("model_accuracy", 0),
                "recommendation_quality": feedback_data.get("recommendation_quality", 0)
            }

            # في التطبيق الحقيقي، يمكن حفظ هذه المقاييس في قاعدة البيانات
            print(f"📈 Performance metrics: {performance_metrics}")

        except Exception as e:
            print(f"Error tracking model performance: {e}")

    def get_model_performance_report(self) -> Dict[str, Any]:
        """
        الحصول على تقرير أداء النماذج
        """
        try:
            # الحصول على معلومات النماذج من مدير النماذج
            ml_info = ml_manager.get_model_performance()

            # إضافة معلومات إضافية عن الأداء
            report = {
                "ml_models_status": ml_info,
                "knowledge_base_status": self.knowledge_base.get_status(),
                "hybrid_system_status": {
                    "rules_available": len(self.knowledge_base.get_all_rules()),
                    "models_loaded": len(ml_info["loaded_models"]),
                    "system_ready": len(ml_info["loaded_models"]) > 0
                }
            }

            return report
        except Exception as e:
            print(f"Error generating performance report: {e}")
            return {"error": str(e)}
