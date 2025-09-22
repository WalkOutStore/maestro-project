from typing import Dict, Any, List, Optional, Tuple
import numpy as np
import pandas as pd
import joblib
import os
from sqlalchemy.orm import Session

from app.core.strategic_mind.knowledge_base import DynamicKnowledgeBase
from app.models.knowledge_base import MLModel
from app.config import settings


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
        التنبؤ بمعدل النقر إلى الظهور (CTR) باستخدام النموذج الهجين
        """
        # استخدام البيانات النموذجية إذا لم تكن النماذج متاحة
        from app.core.strategic_mind.mock_data import generate_ctr_prediction
        
        # استخدام القواعد الرمزية أولاً
        rule_actions = self.knowledge_base.evaluate_rules(campaign_data, rule_type="ctr_prediction")
        
        # استخدام نموذج التعلم الآلي إذا كان متاحًا
        ml_prediction = None
        confidence = 0.0
        explanation = []
        
        if "ctr_prediction" in self.ml_models:
            ml_model_info = self.ml_models["ctr_prediction"]
            model = ml_model_info["model"]
            features = ml_model_info["features"]
            
            # تحضير البيانات للنموذج
            X = self._prepare_features(campaign_data, features)
            
            if X is not None:
                try:
                    # التنبؤ باستخدام النموذج
                    ml_prediction = float(model.predict(X)[0])
                    
                    # حساب الثقة (يمكن تنفيذ منطق أكثر تعقيدًا)
                    confidence = 0.8  # قيمة افتراضية
                    
                    # إضافة تفسير من النموذج
                    explanation.append({
                        "source": "ml_model",
                        "factor": "model_prediction",
                        "importance": 0.8,
                        "description": f"ML model predicted CTR of {ml_prediction:.4f}"
                    })
                except Exception as e:
                    print(f"Error predicting CTR with ML model: {e}")
        
        # إذا لم تكن النماذج متاحة، استخدم البيانات النموذجية
        if ml_prediction is None and not rule_actions:
            return generate_ctr_prediction(campaign_data)
        
        # دمج النتائج من القواعد الرمزية ونموذج التعلم الآلي
        final_prediction = self._combine_predictions(rule_actions, ml_prediction)
        
        # إضافة تفسيرات من القواعد الرمزية
        for action in rule_actions:
            if "ctr_factor" in action["actions"]:
                explanation.append({
                    "source": "symbolic_rule",
                    "factor": action["rule_name"],
                    "importance": 0.5,  # يمكن تعديل هذه القيمة
                    "description": action["actions"].get("explanation", "Rule-based factor")
                })
        
        return {
            "prediction": final_prediction,
            "confidence": confidence,
            "explanation": explanation
        }
    
    def predict_roi(self, campaign_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        التنبؤ بالعائد على الاستثمار (ROI) باستخدام النموذج الهجين
        """
        # استخدام البيانات النموذجية إذا لم تكن النماذج متاحة
        from app.core.strategic_mind.mock_data import generate_roi_prediction
        
        # استخدام القواعد الرمزية أولاً
        rule_actions = self.knowledge_base.evaluate_rules(campaign_data, rule_type="roi_prediction")
        
        # استخدام نموذج التعلم الآلي إذا كان متاحًا
        ml_prediction = None
        confidence = 0.0
        explanation = []
        
        if "roi_prediction" in self.ml_models:
            ml_model_info = self.ml_models["roi_prediction"]
            model = ml_model_info["model"]
            features = ml_model_info["features"]
            
            # تحضير البيانات للنموذج
            X = self._prepare_features(campaign_data, features)
            
            if X is not None:
                try:
                    # التنبؤ باستخدام النموذج
                    ml_prediction = float(model.predict(X)[0])
                    
                    # حساب الثقة (يمكن تنفيذ منطق أكثر تعقيدًا)
                    confidence = 0.8  # قيمة افتراضية
                    
                    # إضافة تفسير من النموذج
                    explanation.append({
                        "source": "ml_model",
                        "factor": "model_prediction",
                        "importance": 0.8,
                        "description": f"ML model predicted ROI of {ml_prediction:.2f}%"
                    })
                except Exception as e:
                    print(f"Error predicting ROI with ML model: {e}")
        
        # إذا لم تكن النماذج متاحة، استخدم البيانات النموذجية
        if ml_prediction is None and not rule_actions:
            return generate_roi_prediction(campaign_data)
        
        # دمج النتائج من القواعد الرمزية ونموذج التعلم الآلي
        final_prediction = self._combine_predictions(rule_actions, ml_prediction)
        
        # إضافة تفسيرات من القواعد الرمزية
        for action in rule_actions:
            if "roi_factor" in action["actions"]:
                explanation.append({
                    "source": "symbolic_rule",
                    "factor": action["rule_name"],
                    "importance": 0.5,  # يمكن تعديل هذه القيمة
                    "description": action["actions"].get("explanation", "Rule-based factor")
                })
        
        return {
            "prediction": final_prediction,
            "confidence": confidence,
            "explanation": explanation
        }
    
    def recommend_channels(self, campaign_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        توصية بقنوات التسويق المناسبة للحملة
        """
        # استخدام البيانات النموذجية إذا لم تكن النماذج متاحة
        from app.core.strategic_mind.mock_data import generate_channel_recommendations
        
        # استخدام القواعد الرمزية
        rule_actions = self.knowledge_base.evaluate_rules(campaign_data, rule_type="channel_recommendation")
        
        recommendations = []
        for action in rule_actions:
            if "recommended_channels" in action["actions"]:
                for channel in action["actions"]["recommended_channels"]:
                    recommendations.append({
                        "channel": channel,
                        "score": action["actions"].get("score", 0.5),
                        "reason": action["actions"].get("reason", "Based on rule: " + action["rule_name"])
                    })
        
        # استخدام نموذج التعلم الآلي إذا كان متاحًا
        if "channel_recommendation" in self.ml_models:
            ml_model_info = self.ml_models["channel_recommendation"]
            model = ml_model_info["model"]
            features = ml_model_info["features"]
            
            # تحضير البيانات للنموذج
            X = self._prepare_features(campaign_data, features)
            
            if X is not None:
                try:
                    # التنبؤ باستخدام النموذج
                    # هذا مثال بسيط، يمكن تنفيذ منطق أكثر تعقيدًا
                    channel_scores = model.predict_proba(X)[0]
                    channels = model.classes_
                    
                    for i, channel in enumerate(channels):
                        recommendations.append({
                            "channel": channel,
                            "score": float(channel_scores[i]),
                            "reason": f"ML model prediction with {channel_scores[i]:.2f} confidence"
                        })
                except Exception as e:
                    print(f"Error recommending channels with ML model: {e}")
        
        # إذا لم تكن هناك توصيات من القواعد أو النماذج، استخدم البيانات النموذجية
        if not recommendations:
            return generate_channel_recommendations(campaign_data)
        
        # ترتيب التوصيات حسب الدرجة
        recommendations.sort(key=lambda x: x["score"], reverse=True)
        
        return recommendations
    
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
            if "prediction" in action["actions"]:
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
        تحديث النماذج بناءً على التغذية الراجعة
        """
        # تحديث القواعد الرمزية
        if "rule_feedback" in feedback_data:
            for rule_feedback in feedback_data["rule_feedback"]:
                rule_id = rule_feedback.get("rule_id")
                if rule_id:
                    self.knowledge_base.update_from_feedback(rule_id, rule_feedback)
        
        # تحديث نماذج التعلم الآلي
        # هذا يتطلب إعادة تدريب النماذج، وهو عملية معقدة
        # يمكن تنفيذ منطق بسيط هنا وترك التفاصيل لوحدة منفصلة
        
        return True
