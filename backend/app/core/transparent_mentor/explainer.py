from typing import Dict, Any, List, Optional, Tuple
import numpy as np
import pandas as pd
import json
import os
from sqlalchemy.orm import Session

from app.config import settings


class DecisionExplainer:
    """
    شارح القرارات الذي يوفر تفسيرات شفافة للتوصيات والتنبؤات
    """
    
    def __init__(self, db: Session = None):
        """
        تهيئة شارح القرارات
        """
        self.db = db
    
    def explain_prediction(self, prediction_data: Dict[str, Any], model_type: str) -> Dict[str, Any]:
        """
        تفسير تنبؤ من نموذج التعلم الآلي
        """
        # استخراج الميزات من البيانات
        features = prediction_data.get("features", {})
        
        # إنشاء تنبؤ بناءً على الميزات الموجودة
        if model_type == "model_v1" and "budget" in features:
            budget = features["budget"]
            # حساب تنبؤ بسيط بناءً على الميزانية
            prediction = min(0.95, max(0.05, (budget / 10000) * 0.3 + 0.1))
            
            explanation = [
                {
                    "source": "model",
                    "factor": "budget_impact",
                    "importance": 0.6,
                    "value": budget,
                    "description": f"الميزانية المحددة ({budget:,} دولار) تؤثر بشكل كبير على التنبؤ"
                },
                {
                    "source": "model", 
                    "factor": "market_conditions",
                    "importance": 0.25,
                    "value": "stable",
                    "description": "ظروف السوق الحالية مستقرة"
                },
                {
                    "source": "model",
                    "factor": "historical_performance", 
                    "importance": 0.15,
                    "value": "average",
                    "description": "الأداء التاريخي للحملات المشابهة"
                }
            ]
            
            return {
                "prediction": prediction,
                "confidence": 0.85,
                "explanation": explanation,
                "visualization_data": self._prepare_visualization_data(explanation, model_type)
            }
        
        # إذا لم تكن هناك ميزات كافية، إرجاع تفسير افتراضي
        explanation = self._generate_default_explanation(prediction_data, model_type)
        
        return {
            "prediction": 0.3,
            "confidence": 0.7,
            "explanation": explanation,
            "visualization_data": self._prepare_visualization_data(explanation, model_type)
        }
    
    def explain_recommendation(self, recommendation_data: Dict[str, Any], recommendation_type: str) -> Dict[str, Any]:
        """
        تفسير توصية من النظام
        """
        # التحقق من وجود تفسير في البيانات
        if "explanation" in recommendation_data:
            return {
                "explanation": recommendation_data["explanation"],
                "visualization_data": self._prepare_visualization_data(recommendation_data["explanation"], recommendation_type)
            }
        
        # إذا لم يكن هناك تفسير، إنشاء تفسير افتراضي
        explanation = self._generate_default_explanation(recommendation_data, recommendation_type)
        
        return {
            "explanation": explanation,
            "visualization_data": self._prepare_visualization_data(explanation, recommendation_type)
        }
    
    def generate_alternative_scenarios(self, base_data: Dict[str, Any], scenario_type: str, num_scenarios: int = 3) -> List[Dict[str, Any]]:
        """
        توليد سيناريوهات بديلة لمساعدة المستخدم في فهم تأثير التغييرات
        """
        scenarios = []
        
        if scenario_type == "budget_allocation":
            # توليد سيناريوهات بديلة لتخصيص الميزانية
            base_budget = base_data.get("budget", 1000)
            base_channels = base_data.get("channels", {})
            
            # سيناريو 1: زيادة الميزانية بنسبة 20%
            scenario1 = base_data.copy()
            scenario1["budget"] = base_budget * 1.2
            scenario1["expected_roi"] = base_data.get("expected_roi", 0) * 1.15  # زيادة العائد المتوقع
            scenario1["description"] = "Increase budget by 20%"
            scenario1["changes"] = [{"factor": "budget", "change": "+20%"}]
            scenarios.append(scenario1)
            
            # سيناريو 2: تغيير توزيع الميزانية بين القنوات
            if base_channels:
                scenario2 = base_data.copy()
                new_channels = {}
                for channel, amount in base_channels.items():
                    if channel == list(base_channels.keys())[0]:  # زيادة الميزانية للقناة الأولى
                        new_channels[channel] = amount * 1.3
                    elif channel == list(base_channels.keys())[1]:  # تقليل الميزانية للقناة الثانية
                        new_channels[channel] = amount * 0.7
                    else:
                        new_channels[channel] = amount
                scenario2["channels"] = new_channels
                scenario2["description"] = f"Reallocate budget: +30% to {list(base_channels.keys())[0]}, -30% from {list(base_channels.keys())[1]}"
                scenario2["changes"] = [
                    {"factor": f"budget_{list(base_channels.keys())[0]}", "change": "+30%"},
                    {"factor": f"budget_{list(base_channels.keys())[1]}", "change": "-30%"}
                ]
                scenarios.append(scenario2)
            
            # سيناريو 3: تركيز الميزانية على القناة الأفضل أداءً
            if base_channels:
                scenario3 = base_data.copy()
                best_channel = max(base_channels.items(), key=lambda x: x[1])
                new_channels = {}
                for channel, amount in base_channels.items():
                    if channel == best_channel[0]:
                        new_channels[channel] = amount * 1.5
                    else:
                        new_channels[channel] = amount * 0.8
                scenario3["channels"] = new_channels
                scenario3["description"] = f"Focus budget on best performing channel: {best_channel[0]}"
                scenario3["changes"] = [
                    {"factor": f"budget_{best_channel[0]}", "change": "+50%"},
                    {"factor": "budget_other_channels", "change": "-20%"}
                ]
                scenarios.append(scenario3)
        
        elif scenario_type == "content_strategy":
            # توليد سيناريوهات بديلة لاستراتيجية المحتوى
            base_content_types = base_data.get("content_types", {})
            
            # سيناريو 1: زيادة المحتوى المرئي
            scenario1 = base_data.copy()
            new_content_types = base_content_types.copy() if base_content_types else {"text": 0.5, "image": 0.3, "video": 0.2}
            new_content_types["image"] = new_content_types.get("image", 0) + 0.2
            new_content_types["video"] = new_content_types.get("video", 0) + 0.1
            new_content_types["text"] = max(0, new_content_types.get("text", 0) - 0.3)
            # تطبيع القيم
            total = sum(new_content_types.values())
            new_content_types = {k: v / total for k, v in new_content_types.items()}
            scenario1["content_types"] = new_content_types
            scenario1["description"] = "Increase visual content (images and videos)"
            scenario1["changes"] = [
                {"factor": "image_content", "change": "+20%"},
                {"factor": "video_content", "change": "+10%"},
                {"factor": "text_content", "change": "-30%"}
            ]
            scenarios.append(scenario1)
            
            # سيناريو 2: زيادة المحتوى التفاعلي
            scenario2 = base_data.copy()
            new_content_types = base_content_types.copy() if base_content_types else {"text": 0.4, "image": 0.3, "video": 0.2, "interactive": 0.1}
            new_content_types["interactive"] = new_content_types.get("interactive", 0) + 0.2
            new_content_types["text"] = max(0, new_content_types.get("text", 0) - 0.1)
            new_content_types["image"] = max(0, new_content_types.get("image", 0) - 0.1)
            # تطبيع القيم
            total = sum(new_content_types.values())
            new_content_types = {k: v / total for k, v in new_content_types.items()}
            scenario2["content_types"] = new_content_types
            scenario2["description"] = "Increase interactive content"
            scenario2["changes"] = [
                {"factor": "interactive_content", "change": "+20%"},
                {"factor": "text_content", "change": "-10%"},
                {"factor": "image_content", "change": "-10%"}
            ]
            scenarios.append(scenario2)
            
            # سيناريو 3: التركيز على المحتوى القصير
            scenario3 = base_data.copy()
            scenario3["content_length"] = "short"
            scenario3["posting_frequency"] = base_data.get("posting_frequency", 1) * 1.5
            scenario3["description"] = "Focus on short-form content with higher frequency"
            scenario3["changes"] = [
                {"factor": "content_length", "change": "short"},
                {"factor": "posting_frequency", "change": "+50%"}
            ]
            scenarios.append(scenario3)
        
        elif scenario_type == "targeting":
            # توليد سيناريوهات بديلة للاستهداف
            base_audience = base_data.get("target_audience", {})
            
            # سيناريو 1: توسيع نطاق الجمهور المستهدف
            scenario1 = base_data.copy()
            new_audience = base_audience.copy() if base_audience else {"age_range": [25, 45], "interests": ["technology"]}
            if "age_range" in new_audience:
                new_audience["age_range"] = [max(18, new_audience["age_range"][0] - 5), new_audience["age_range"][1] + 5]
            scenario1["target_audience"] = new_audience
            scenario1["reach"] = base_data.get("reach", 1000) * 1.4
            scenario1["conversion_rate"] = base_data.get("conversion_rate", 0.02) * 0.9
            scenario1["description"] = "Expand target audience age range"
            scenario1["changes"] = [
                {"factor": "age_range", "change": "wider"},
                {"factor": "reach", "change": "+40%"},
                {"factor": "conversion_rate", "change": "-10%"}
            ]
            scenarios.append(scenario1)
            
            # سيناريو 2: تضييق نطاق الجمهور المستهدف
            scenario2 = base_data.copy()
            new_audience = base_audience.copy() if base_audience else {"age_range": [25, 45], "interests": ["technology"]}
            if "age_range" in new_audience:
                new_audience["age_range"] = [new_audience["age_range"][0] + 5, max(new_audience["age_range"][0] + 10, new_audience["age_range"][1] - 5)]
            scenario2["target_audience"] = new_audience
            scenario2["reach"] = base_data.get("reach", 1000) * 0.6
            scenario2["conversion_rate"] = base_data.get("conversion_rate", 0.02) * 1.3
            scenario2["description"] = "Narrow target audience age range"
            scenario2["changes"] = [
                {"factor": "age_range", "change": "narrower"},
                {"factor": "reach", "change": "-40%"},
                {"factor": "conversion_rate", "change": "+30%"}
            ]
            scenarios.append(scenario2)
            
            # سيناريو 3: إضافة اهتمامات جديدة
            scenario3 = base_data.copy()
            new_audience = base_audience.copy() if base_audience else {"age_range": [25, 45], "interests": ["technology"]}
            if "interests" in new_audience:
                new_interests = new_audience["interests"].copy()
                new_interests.extend(["innovation", "digital trends"])
                new_audience["interests"] = list(set(new_interests))
            else:
                new_audience["interests"] = ["technology", "innovation", "digital trends"]
            scenario3["target_audience"] = new_audience
            scenario3["reach"] = base_data.get("reach", 1000) * 1.2
            scenario3["description"] = "Add new interest targeting"
            scenario3["changes"] = [
                {"factor": "interests", "change": "added innovation, digital trends"},
                {"factor": "reach", "change": "+20%"}
            ]
            scenarios.append(scenario3)
        
        # ترتيب السيناريوهات حسب التأثير المتوقع
        scenarios.sort(key=lambda x: x.get("expected_roi", 0), reverse=True)
        
        # اقتصار العدد على العدد المطلوب
        return scenarios[:num_scenarios]
    
    def _generate_default_explanation(self, data: Dict[str, Any], explanation_type: str) -> List[Dict[str, Any]]:
        """
        توليد تفسير افتراضي بناءً على نوع التفسير
        """
        explanation = []
        
        if explanation_type == "ctr_prediction":
            # تفسير افتراضي لتنبؤ معدل النقر إلى الظهور
            prediction = data.get("prediction", 0)
            
            explanation.append({
                "source": "model",
                "factor": "industry_average",
                "importance": 0.4,
                "description": f"Industry average CTR is {prediction * 0.8:.4f}"
            })
            
            explanation.append({
                "source": "model",
                "factor": "creative_quality",
                "importance": 0.3,
                "description": "Creative quality assessment based on historical performance"
            })
            
            explanation.append({
                "source": "model",
                "factor": "targeting_precision",
                "importance": 0.2,
                "description": "Audience targeting precision score"
            })
            
            explanation.append({
                "source": "model",
                "factor": "seasonal_trends",
                "importance": 0.1,
                "description": "Seasonal trends adjustment"
            })
        
        elif explanation_type == "roi_prediction":
            # تفسير افتراضي لتنبؤ العائد على الاستثمار
            prediction = data.get("prediction", 0)
            
            explanation.append({
                "source": "model",
                "factor": "historical_performance",
                "importance": 0.35,
                "description": f"Based on historical campaign performance in similar conditions"
            })
            
            explanation.append({
                "source": "model",
                "factor": "industry_benchmark",
                "importance": 0.25,
                "description": f"Industry benchmark ROI is {prediction * 0.9:.2f}%"
            })
            
            explanation.append({
                "source": "model",
                "factor": "channel_efficiency",
                "importance": 0.2,
                "description": "Channel efficiency scores based on past campaigns"
            })
            
            explanation.append({
                "source": "model",
                "factor": "budget_allocation",
                "importance": 0.2,
                "description": "Budget allocation optimization across channels"
            })
        
        elif explanation_type == "channel_recommendation":
            # تفسير افتراضي لتوصية القنوات
            channels = data.get("channel", [])
            if isinstance(channels, str):
                channels = [channels]
            
            for i, channel in enumerate(channels):
                importance = 0.8 - (i * 0.2)
                if importance > 0:
                    explanation.append({
                        "source": "model",
                        "factor": f"{channel}_performance",
                        "importance": importance,
                        "description": f"Historical performance of {channel} for similar campaigns"
                    })
            
            explanation.append({
                "source": "model",
                "factor": "audience_presence",
                "importance": 0.3,
                "description": "Target audience presence on recommended channels"
            })
            
            explanation.append({
                "source": "model",
                "factor": "cost_efficiency",
                "importance": 0.2,
                "description": "Cost efficiency analysis across available channels"
            })
        
        elif explanation_type == "content_recommendation":
            # تفسير افتراضي لتوصية المحتوى
            explanation.append({
                "source": "model",
                "factor": "engagement_prediction",
                "importance": 0.4,
                "description": "Predicted engagement based on content characteristics"
            })
            
            explanation.append({
                "source": "model",
                "factor": "audience_preferences",
                "importance": 0.3,
                "description": "Target audience content preferences analysis"
            })
            
            explanation.append({
                "source": "model",
                "factor": "trend_alignment",
                "importance": 0.2,
                "description": "Alignment with current market trends"
            })
            
            explanation.append({
                "source": "model",
                "factor": "brand_consistency",
                "importance": 0.1,
                "description": "Consistency with brand voice and messaging"
            })
        
        return explanation
    
    def _prepare_visualization_data(self, explanation: List[Dict[str, Any]], visualization_type: str) -> Dict[str, Any]:
        """
        تحضير بيانات التصور المرئي للتفسير
        """
        visualization_data = {
            "type": visualization_type,
            "factors": [],
            "importance": [],
            "descriptions": []
        }
        
        # استخراج البيانات من التفسير
        for item in explanation:
            visualization_data["factors"].append(item["factor"])
            visualization_data["importance"].append(item["importance"])
            visualization_data["descriptions"].append(item["description"])
        
        # إضافة بيانات إضافية حسب نوع التصور
        if visualization_type == "ctr_prediction" or visualization_type == "roi_prediction":
            visualization_data["chart_type"] = "waterfall"
        elif visualization_type == "channel_recommendation":
            visualization_data["chart_type"] = "bar"
        elif visualization_type == "content_recommendation":
            visualization_data["chart_type"] = "radar"
        else:
            visualization_data["chart_type"] = "bar"
        
        return visualization_data
