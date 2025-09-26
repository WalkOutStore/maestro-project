#!/usr/bin/env python3
"""
مدير نماذج التعلم الآلي - يعتمد فقط على النماذج الحقيقية
"""

import os
import joblib
import pickle
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score


class MLModelManager:
    """
    مدير نماذج التعلم الآلي يعتمد فقط على النماذج الحقيقية
    """

    def __init__(self, models_path: str = "./ml_models"):
        self.models_path = models_path
        self.models = {}
        self.scalers = {}
        self.features = {}
        self._load_existing_models()

    def _load_existing_models(self) -> None:
        """تحميل النماذج الموجودة من الملفات فقط"""
        print("🤖 Loading ML Models...")

        for model_type in ["ctr", "roi", "channel"]:
            model_file = f"{self.models_path}/{model_type}_model.pkl"
            feature_file = f"{self.models_path}/{model_type}_features.pkl"

            if os.path.exists(model_file) and os.path.exists(feature_file):
                try:
                    with open(model_file, 'rb') as f:
                        self.models[model_type] = pickle.load(f)
                    with open(feature_file, 'rb') as f:
                        self.features[model_type] = pickle.load(f)
                    print(f"  ✅ {model_type.upper()} Model loaded")
                except Exception as e:
                    print(f"  ❌ Error loading {model_type} model: {e}")

    def predict_ctr(self, campaign_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """تنبؤ CTR باستخدام النموذج الحقيقي فقط"""
        if "ctr" not in self.models:
            raise ValueError("CTR model not loaded")

        features = self._prepare_features(campaign_data, "ctr")
        if features is None:
            raise ValueError("Insufficient features for CTR prediction")

        model = self.models["ctr"]
        prediction = float(model.predict([features])[0])

        return {"prediction": max(0.0, min(1.0, prediction)), "model_used": "ctr_model"}

    def predict_roi(self, campaign_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """تنبؤ ROI باستخدام النموذج الحقيقي فقط"""
        if "roi" not in self.models:
            raise ValueError("ROI model not loaded")

        features = self._prepare_features(campaign_data, "roi")
        if features is None:
            raise ValueError("Insufficient features for ROI prediction")

        # تطبيع البيانات إذا كان scaler متوفر
        if "roi" in self.scalers:
            features = self.scalers["roi"].transform([features])[0]

        model = self.models["roi"]
        prediction = float(model.predict([features])[0])

        return {"prediction": max(0.0, prediction), "model_used": "roi_model"}

    def recommend_channels(self, campaign_data: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
        """توصية القنوات باستخدام النموذج الحقيقي فقط"""
        if "channel" not in self.models:
            raise ValueError("Channel model not loaded")

        features = self._prepare_features(campaign_data, "channel")
        if features is None:
            raise ValueError("Insufficient features for channel recommendation")

        model = self.models["channel"]
        scores = model.predict([features])[0]

        channels = ["facebook", "instagram", "google_ads", "twitter", "linkedin", "youtube"]
        recommendations = []

        for i, channel in enumerate(channels):
            if i < len(scores):
                recommendations.append({
                    "channel": channel,
                    "score": max(0.0, min(1.0, float(scores[i])))
                })

        recommendations.sort(key=lambda x: x["score"], reverse=True)
        return recommendations[:5]

    def _prepare_features(self, campaign_data: Dict[str, Any], model_type: str) -> Optional[List[float]]:
        """تحضير ميزات الحملة من البيانات الحقيقية"""
        if model_type not in self.features:
            return None

        feature_values = []
        for feature in self.features[model_type]:
            if feature not in campaign_data:
                return None  # إرجاع None إذا أي ميزة ناقصة
            value = campaign_data[feature]
            if isinstance(value, bool):
                value = 1.0 if value else 0.0
            elif isinstance(value, str):
                try:
                    value = float(value)
                except:
                    value = 0.0
            feature_values.append(float(value))

        return feature_values

    def get_model_performance(self) -> Dict[str, Any]:
        """إرجاع معلومات النماذج المحملة"""
        return {
            "loaded_models": list(self.models.keys()),
            "available_features": list(self.features.keys()),
            "scalers_available": list(self.scalers.keys())
        }

    def train_and_save_model(self, model_type: str, training_data: pd.DataFrame, target: str) -> bool:
        """تدريب وحفظ نموذج جديد"""
        try:
            if model_type == "ctr":
                model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
            elif model_type in ["roi", "channel"]:
                model = GradientBoostingRegressor(n_estimators=100, max_depth=5, random_state=42)
            else:
                return False

            X = training_data.drop(columns=[target])
            y = training_data[target]
            model.fit(X, y)

            with open(f"{self.models_path}/{model_type}_model.pkl", "wb") as f:
                pickle.dump(model, f)
            with open(f"{self.models_path}/{model_type}_features.pkl", "wb") as f:
                pickle.dump(list(X.columns), f)

            self.models[model_type] = model
            self.features[model_type] = list(X.columns)

            return True
        except Exception as e:
            print(f"Error training model {model_type}: {e}")
            return False


# إنشاء instance عام
ml_manager = MLModelManager()
