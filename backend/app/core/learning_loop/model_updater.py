from typing import Dict, Any, List, Optional, Tuple
import numpy as np
import pandas as pd
import joblib
import os
from datetime import datetime
from sqlalchemy.orm import Session

from app.models.knowledge_base import MLModel
from app.core.learning_loop.feedback import FeedbackProcessor
from app.config import settings


class ModelUpdater:
    """
    محدث النماذج الذي يستخدم التغذية الراجعة لتحسين نماذج التعلم الآلي
    """
    
    def __init__(self, db: Session = None):
        """
        تهيئة محدث النماذج
        """
        self.db = db
        self.feedback_processor = FeedbackProcessor(db)
    
    def update_model(self, model_type: str, update_params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        تحديث نموذج التعلم الآلي بناءً على التغذية الراجعة
        """
        # التحقق من وجود النموذج
        if self.db:
            model = self.db.query(MLModel).filter(
                MLModel.model_type == model_type,
                MLModel.is_active == True
            ).first()
            
            if not model:
                return {"success": False, "error": "Model not found"}
            
            # الحصول على بيانات التغذية الراجعة
            feedback_data = self.feedback_processor.get_feedback_for_model_update(model_type)
            
            if not feedback_data:
                return {"success": False, "error": "No feedback data available"}
            
            # تحضير البيانات للتدريب
            X, y = self._prepare_training_data(feedback_data, model_type)
            
            if X is None or y is None:
                return {"success": False, "error": "Failed to prepare training data"}
            
            # تحميل النموذج الحالي
            try:
                current_model = joblib.load(model.model_path)
            except Exception as e:
                return {"success": False, "error": f"Failed to load model: {str(e)}"}
            
            # تحديث النموذج
            try:
                updated_model = self._update_model_with_data(current_model, X, y, update_params)
            except Exception as e:
                return {"success": False, "error": f"Failed to update model: {str(e)}"}
            
            # حفظ النموذج المحدث
            new_version = self._increment_version(model.version)
            new_model_path = os.path.join(
                os.path.dirname(model.model_path),
                f"{model_type}_{new_version}.joblib"
            )
            
            try:
                joblib.dump(updated_model, new_model_path)
            except Exception as e:
                return {"success": False, "error": f"Failed to save updated model: {str(e)}"}
            
            # تقييم النموذج المحدث
            performance_metrics = self._evaluate_model(updated_model, X, y)
            
            # إنشاء نموذج جديد في قاعدة البيانات
            new_model = MLModel(
                name=f"{model.name} (v{new_version})",
                description=f"Updated version of {model.name} based on user feedback",
                model_type=model_type,
                model_path=new_model_path,
                features=model.features,
                performance_metrics=performance_metrics,
                version=new_version,
                is_active=True
            )
            
            # تعطيل النموذج القديم
            model.is_active = False
            
            # حفظ التغييرات في قاعدة البيانات
            self.db.add(new_model)
            self.db.commit()
            
            return {
                "success": True,
                "model_id": new_model.id,
                "version": new_version,
                "performance_metrics": performance_metrics
            }
        
        return {"success": False, "error": "Database not available"}
    
    def _prepare_training_data(self, feedback_data: List[Dict[str, Any]], model_type: str) -> Tuple[Optional[np.ndarray], Optional[np.ndarray]]:
        """
        تحضير بيانات التدريب من التغذية الراجعة
        """
        try:
            # تحويل بيانات التغذية الراجعة إلى DataFrame
            df = pd.DataFrame(feedback_data)
            
            # استخراج الميزات والأهداف بناءً على نوع النموذج
            if model_type == "ctr_prediction":
                # استخراج الميزات من بيانات التوصية
                features = []
                for data in df["recommendation_data"]:
                    # استخراج الميزات ذات الصلة
                    feature_dict = {}
                    if "campaign" in data:
                        feature_dict["industry"] = data["campaign"].get("industry", "unknown")
                        feature_dict["channel"] = data["campaign"].get("channel", "unknown")
                        feature_dict["audience_age"] = data["campaign"].get("audience_age", 0)
                        feature_dict["budget"] = data["campaign"].get("budget", 0)
                    features.append(feature_dict)
                
                features_df = pd.DataFrame(features)
                
                # تحويل الميزات النصية إلى متغيرات وهمية
                features_df = pd.get_dummies(features_df, columns=["industry", "channel"])
                
                # استخدام التقييم كهدف
                y = df["rating"].values
                
                # تحويل الميزات إلى مصفوفة
                X = features_df.values
                
                return X, y
            
            elif model_type == "roi_prediction":
                # استخراج الميزات من بيانات التوصية
                features = []
                for data in df["recommendation_data"]:
                    # استخراج الميزات ذات الصلة
                    feature_dict = {}
                    if "campaign" in data:
                        feature_dict["industry"] = data["campaign"].get("industry", "unknown")
                        feature_dict["channel"] = data["campaign"].get("channel", "unknown")
                        feature_dict["budget"] = data["campaign"].get("budget", 0)
                        feature_dict["duration"] = data["campaign"].get("duration", 0)
                    features.append(feature_dict)
                
                features_df = pd.DataFrame(features)
                
                # تحويل الميزات النصية إلى متغيرات وهمية
                features_df = pd.get_dummies(features_df, columns=["industry", "channel"])
                
                # استخدام التقييم كهدف
                y = df["rating"].values
                
                # تحويل الميزات إلى مصفوفة
                X = features_df.values
                
                return X, y
            
            elif model_type == "channel_recommendation":
                # استخراج الميزات من بيانات التوصية
                features = []
                for data in df["recommendation_data"]:
                    # استخراج الميزات ذات الصلة
                    feature_dict = {}
                    if "campaign" in data:
                        feature_dict["industry"] = data["campaign"].get("industry", "unknown")
                        feature_dict["audience_age"] = data["campaign"].get("audience_age", 0)
                        feature_dict["budget"] = data["campaign"].get("budget", 0)
                    features.append(feature_dict)
                
                features_df = pd.DataFrame(features)
                
                # تحويل الميزات النصية إلى متغيرات وهمية
                features_df = pd.get_dummies(features_df, columns=["industry"])
                
                # استخدام التقييم كهدف
                y = df["rating"].values
                
                # تحويل الميزات إلى مصفوفة
                X = features_df.values
                
                return X, y
            
            else:
                # نوع نموذج غير معروف
                return None, None
        
        except Exception as e:
            print(f"Error preparing training data: {str(e)}")
            return None, None
    
    def _update_model_with_data(self, model: Any, X: np.ndarray, y: np.ndarray, update_params: Dict[str, Any] = None) -> Any:
        """
        تحديث النموذج باستخدام البيانات الجديدة
        """
        # التحقق من نوع النموذج وتحديثه وفقًا لذلك
        # هذا مثال بسيط، يمكن توسيعه حسب أنواع النماذج المستخدمة
        
        try:
            # تحديث النموذج باستخدام البيانات الجديدة
            if hasattr(model, "partial_fit"):
                # استخدام التعلم التدريجي إذا كان متاحًا
                model.partial_fit(X, y)
            else:
                # إعادة تدريب النموذج بالكامل
                # يمكن دمج البيانات القديمة والجديدة هنا إذا لزم الأمر
                if update_params:
                    model.fit(X, y, **update_params)
                else:
                    model.fit(X, y)
            
            return model
        
        except Exception as e:
            print(f"Error updating model: {str(e)}")
            raise
    
    def _evaluate_model(self, model: Any, X: np.ndarray, y: np.ndarray) -> Dict[str, float]:
        """
        تقييم أداء النموذج
        """
        try:
            # التنبؤ باستخدام النموذج
            y_pred = model.predict(X)
            
            # حساب مقاييس الأداء
            mse = np.mean((y - y_pred) ** 2)
            mae = np.mean(np.abs(y - y_pred))
            r2 = 1 - (np.sum((y - y_pred) ** 2) / np.sum((y - np.mean(y)) ** 2))
            
            return {
                "mse": float(mse),
                "mae": float(mae),
                "r2": float(r2)
            }
        
        except Exception as e:
            print(f"Error evaluating model: {str(e)}")
            return {
                "mse": 0.0,
                "mae": 0.0,
                "r2": 0.0
            }
    
    def _increment_version(self, version: str) -> str:
        """
        زيادة رقم إصدار النموذج
        """
        try:
            # تقسيم الإصدار إلى أجزاء
            parts = version.split(".")
            
            # زيادة الجزء الأخير
            if len(parts) > 0:
                parts[-1] = str(int(parts[-1]) + 1)
            else:
                parts = ["1", "0"]
            
            # إعادة تجميع الإصدار
            return ".".join(parts)
        
        except Exception:
            # إذا حدث خطأ، إرجاع إصدار افتراضي
            return "1.0"
    
    def schedule_model_update(self, model_type: str, schedule: Dict[str, Any]) -> Dict[str, Any]:
        """
        جدولة تحديث النموذج
        """
        # هذه الدالة يمكن أن تجدول تحديث النموذج في وقت محدد
        # مثل تحديث النموذج كل أسبوع أو عند توفر عدد معين من التغذيات الراجعة
        
        # هذا مثال بسيط، يمكن توسيعه حسب احتياجات المشروع
        
        # نعيد معلومات الجدولة
        return {
            "model_type": model_type,
            "schedule": schedule,
            "next_update": datetime.now().isoformat()
        }
