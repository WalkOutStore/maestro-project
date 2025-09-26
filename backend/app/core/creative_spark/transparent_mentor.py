from typing import Dict, Any, List, Optional
import requests
import json
import os
import json
try:
    import groq
    from groq import Groq
except ImportError:
    groq = None
    Groq = None
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.knowledge_base import ContentTemplate
from app.config import settings
from app.core.creative_spark.api_integrations import api_integrations


class TransparentMentor:
    def __init__(self, db: Session = None):
        self.db = db

    def _analyze_input_data(self, campaign_data):
        """
        تحليل بيانات الحملة الإعلانية بشكل شامل
        """
        analysis = {
            "campaign_summary": {},
            "target_audience_analysis": {},
            "content_requirements": {},
            "budget_analysis": {},
            "industry_analysis": {},
            "risk_factors": []
        }

        # تحليل بيانات الحملة الأساسية
        analysis["campaign_summary"] = {
            "campaign_name": campaign_data.get("name", "غير محدد"),
            "product_name": campaign_data.get("product_name", "غير محدد"),
            "industry": campaign_data.get("industry", "غير محدد"),
            "goal": campaign_data.get("goal", "غير محدد"),
            "budget": campaign_data.get("budget", 0),
            "duration": campaign_data.get("duration", "غير محدد"),
            "platforms": campaign_data.get("platforms", []),
            "data_completeness": self._calculate_data_completeness(campaign_data)
        }

        # تحليل الجمهور المستهدف
        target_audience = campaign_data.get("target_audience", {})
        analysis["target_audience_analysis"] = {
            "age_range": target_audience.get("age_range", "غير محدد"),
            "gender": target_audience.get("gender", "غير محدد"),
            "interests": target_audience.get("interests", []),
            "locations": target_audience.get("locations", []),
            "audience_size_estimate": self._estimate_audience_size(target_audience),
            "behavioral_insights": self._analyze_audience_behavior(target_audience)
        }

        # تحليل متطلبات المحتوى
        analysis["content_requirements"] = {
            "content_types": campaign_data.get("content_types", ["ad_copy"]),
            "keywords": campaign_data.get("keywords", []),
            "brand_guidelines": campaign_data.get("brand_guidelines", {}),
            "tone": self._determine_content_tone(campaign_data),
            "language": campaign_data.get("language", "العربية"),
            "cultural_considerations": self._analyze_cultural_context(campaign_data)
        }

        # تحليل الميزانية والتكاليف
        analysis["budget_analysis"] = {
            "total_budget": campaign_data.get("budget", 0),
            "budget_allocation": self._analyze_budget_allocation(campaign_data),
            "cost_per_platform": self._calculate_cost_per_platform(campaign_data),
            "efficiency_score": self._calculate_budget_efficiency(campaign_data)
        }

        # تحليل الصناعة والمنافسة
        analysis["industry_analysis"] = {
            "industry_category": campaign_data.get("industry", "غير محدد"),
            "competitive_landscape": self._analyze_competitive_landscape(campaign_data),
            "market_trends": self._get_industry_trends(campaign_data),
            "seasonal_factors": self._analyze_seasonal_factors(campaign_data)
        }

        # تحديد عوامل الخطر
        analysis["risk_factors"] = self._identify_risk_factors(campaign_data)

        return analysis
    def _analyze_confidence_factors(self, prediction_data) -> list:
        if isinstance(prediction_data, list):
            prediction_data = prediction_data[0]  # أخذ أول عنصر إذا كانت قائمة
        features = prediction_data.get("features", {})
        factors = []
        for name, value in features.items():
            factors.append({
                "name": name,
                "value": value,
                "description": f"Factor {name} contributed with value {value}"
            })
        return factors

    def _calculate_data_completeness(self, campaign_data):
        """
        حساب درجة اكتمال البيانات
        """
        required_fields = ["name", "product_name", "industry", "goal", "budget", "target_audience"]
        optional_fields = ["keywords", "platforms", "duration", "brand_guidelines"]

        completed_fields = sum(1 for field in required_fields if campaign_data.get(field))
        optional_completed = sum(1 for field in optional_fields if campaign_data.get(field))

        completeness_score = (completed_fields / len(required_fields)) * 0.7 + (optional_completed / len(optional_fields)) * 0.3
        return round(completeness_score * 100, 1)

    def _estimate_audience_size(self, target_audience):
        """
        تقدير حجم الجمهور المستهدف
        """
        if not target_audience:
            return "غير محدد"

        age_range = target_audience.get("age_range", [18, 65])
        locations = target_audience.get("locations", ["الشرق الأوسط"])

        # تقديرات أساسية (يمكن تحسينها ببيانات حقيقية)
        base_audience = 1000000  # قاعدة أساسية

        # تعديل حسب الفئة العمرية
        age_factor = (age_range[1] - age_range[0]) / 50 if len(age_range) == 2 else 1.0

        # تعديل حسب الموقع الجغرافي
        location_multiplier = len(locations) * 0.3 + 1

        estimated_size = int(base_audience * age_factor * location_multiplier)
        return f"{estimated_size:,} تقريباً"

    def _analyze_audience_behavior(self, target_audience):
        """
        تحليل سلوك الجمهور المستهدف
        """
        insights = []

        if target_audience.get("interests"):
            interests = target_audience["interests"]
            insights.append(f"الجمهور مهتم بـ: {', '.join(interests[:3])}")

        if target_audience.get("age_range"):
            age_range = target_audience["age_range"]
            if len(age_range) == 2:
                avg_age = (age_range[0] + age_range[1]) / 2
                if avg_age < 25:
                    insights.append("جمهور شاب يفضل المحتوى التفاعلي والحديث")
                elif avg_age < 40:
                    insights.append("جمهور بالغ يبحث عن القيمة والمصداقية")
                else:
                    insights.append("جمهور ناضج يقدر الجودة والخبرة")

        return insights

    def _determine_content_tone(self, campaign_data):
        """
        تحديد نبرة المحتوى المناسبة
        """
        industry = campaign_data.get("industry", "").lower()
        goal = campaign_data.get("goal", "").lower()

        tone_mapping = {
            "technology": "مبتكر وتقني",
            "fashion": "أنيق وعصري",
            "food": "شهي وجذاب",
            "health": "صحي وموثوق",
            "education": "تعليمي ومفيد",
            "finance": "مهني وموثوق"
        }

        # تحديد النبرة حسب الصناعة
        tone = tone_mapping.get(industry, "محايد وجذاب")

        # تعديل حسب الهدف
        if "awareness" in goal or "brand" in goal:
            tone += " مع التركيز على بناء الوعي"
        elif "conversion" in goal or "sales" in goal:
            tone += " مع التركيز على الإقناع والتحويل"
        elif "engagement" in goal:
            tone += " مع التركيز على التفاعل"

        return tone

    def _analyze_cultural_context(self, campaign_data):
        """
        تحليل السياق الثقافي
        """
        locations = campaign_data.get("target_audience", {}).get("locations", ["الشرق الأوسط"])
        industry = campaign_data.get("industry", "")

        considerations = []

        if "السعودية" in locations or "الشرق الأوسط" in locations:
            considerations.append("مراعاة القيم الثقافية والدينية")
            considerations.append("استخدام لغة محترمة ومهذبة")
            considerations.append("تجنب المحتوى المثير للجدل")

        if industry.lower() in ["food", "restaurant"]:
            considerations.append("مراعاة التقاليد الغذائية والحلال")

        if industry.lower() in ["fashion"]:
            considerations.append("التوازن بين العصرية والاحتشام")

        return considerations

    def _analyze_budget_allocation(self, campaign_data):
        """
        تحليل توزيع الميزانية
        """
        budget = campaign_data.get("budget", 0)
        platforms = campaign_data.get("platforms", [])

        if not platforms:
            return {"error": "لم يتم تحديد المنصات"}

        allocation = {}
        base_allocation = budget / len(platforms)

        for platform in platforms:
            allocation[platform] = round(base_allocation, 2)

        return allocation

    def _calculate_cost_per_platform(self, campaign_data):
        """
        حساب التكلفة لكل منصة
        """
        budget = campaign_data.get("budget", 0)
        platforms = campaign_data.get("platforms", [])

        if not platforms or budget == 0:
            return {}

        cost_per_platform = budget / len(platforms)
        return {platform: round(cost_per_platform, 2) for platform in platforms}

    def _calculate_budget_efficiency(self, campaign_data):
        """
        حساب كفاءة الميزانية
        """
        budget = campaign_data.get("budget", 0)
        target_audience = campaign_data.get("target_audience", {})
        audience_size = self._estimate_audience_size(target_audience)

        if budget == 0:
            return 0

        # تقدير كفاءة الميزانية (بيانات نموذجية)
        efficiency_score = 75  # افتراضي

        if isinstance(audience_size, str) and "تقريباً" in audience_size:
            try:
                audience_num = int(audience_size.split()[0].replace(",", ""))
                cost_per_user = budget / audience_num
                if cost_per_user < 1:
                    efficiency_score = 90
                elif cost_per_user < 5:
                    efficiency_score = 80
                elif cost_per_user < 10:
                    efficiency_score = 70
                else:
                    efficiency_score = 60
            except:
                pass

        return efficiency_score

    def _analyze_competitive_landscape(self, campaign_data):
        """
        تحليل المشهد التنافسي
        """
        industry = campaign_data.get("industry", "")
        keywords = campaign_data.get("keywords", [])

        analysis = {
            "competition_level": "متوسط",
            "key_competitors": [],
            "competitive_advantages": []
        }

        # تحديد مستوى المنافسة حسب الصناعة
        high_competition_industries = ["technology", "fashion", "food", "finance"]
        low_competition_industries = ["education", "health"]

        if industry.lower() in high_competition_industries:
            analysis["competition_level"] = "عالي"
        elif industry.lower() in low_competition_industries:
            analysis["competition_level"] = "منخفض"

        # تحديد المزايا التنافسية
        if keywords:
            analysis["competitive_advantages"] = [
                f"تركيز على: {', '.join(keywords[:3])}",
                "محتوى مخصص ومستهدف",
                "نهج مبني على البيانات"
            ]

        return analysis

    def _get_industry_trends(self, campaign_data):
        """
        الحصول على اتجاهات الصناعة
        """
        industry = campaign_data.get("industry", "")
        keywords = campaign_data.get("keywords", [])

        trends = []

        # اتجاهات عامة حسب الصناعة
        if industry.lower() == "technology":
            trends = ["الذكاء الاصطناعي", "التحول الرقمي", "الأمان السيبراني"]
        elif industry.lower() == "fashion":
            trends = ["الاستدامة", "التسوق عبر الإنترنت", "الموضة السريعة"]
        elif industry.lower() == "food":
            trends = ["المنتجات العضوية", "التوصيل السريع", "الوجبات الصحية"]

        # إضافة الكلمات المفتاحية كاتجاهات محتملة
        if keywords:
            trends.extend(keywords[:2])

        return trends

    def _analyze_seasonal_factors(self, campaign_data):
        """
        تحليل العوامل الموسمية
        """
        # هذا يمكن تطويره لاستخدام بيانات Google Trends الحقيقية
        current_month = datetime.now().month

        seasonal_factors = {
            "current_period": "عادي",
            "recommendations": [],
            "opportunities": []
        }

        # تحديد العوامل الموسمية
        if current_month in [12, 1, 2]:  # الشتاء
            seasonal_factors["current_period"] = "موسم الأعياد والشتاء"
            seasonal_factors["opportunities"] = ["حملات الأعياد", "عروض الشتاء", "هدايا نهاية العام"]
        elif current_month in [6, 7, 8]:  # الصيف
            seasonal_factors["current_period"] = "موسم الصيف"
            seasonal_factors["opportunities"] = ["عروض الصيف", "المنتجات الموسمية", "حملات العطلات"]

        return seasonal_factors

    def _identify_risk_factors(self, campaign_data):
        """
        تحديد عوامل الخطر المحتملة
        """
        risks = []

        # مخاطر البيانات الناقصة
        completeness = self._calculate_data_completeness(campaign_data)
        if completeness < 70:
            risks.append({
                "type": "بيانات ناقصة",
                "severity": "عالية",
                "description": f"اكتمال البيانات {completeness}% فقط",
                "recommendation": "استكمال بيانات الحملة لتحسين النتائج"
            })

        # مخاطر الميزانية
        budget = campaign_data.get("budget", 0)
        if budget < 1000:
            risks.append({
                "type": "ميزانية محدودة",
                "severity": "متوسطة",
                "description": "الميزانية قد لا تكفي للوصول للجمهور المستهدف",
                "recommendation": "زيادة الميزانية أو تقليل نطاق الحملة"
            })

        # مخاطر المنافسة
        industry = campaign_data.get("industry", "")
        if industry.lower() in ["technology", "fashion", "finance"]:
            risks.append({
                "type": "منافسة شديدة",
                "severity": "متوسطة",
                "description": "الصناعة تنافسية جداً",
                "recommendation": "التركيز على المزايا الفريدة والاستهداف الدقيق"
            })

        return risks

    def _explain_template_selection(self, results):
        """
        شرح عملية اختيار القوالب بناءً على النتائج الفعلية
        """
        if not results:
            return {
                "selected_templates": [],
                "selection_criteria": "لم يتم العثور على قوالب مناسبة",
                "reasoning": "عدم وجود نتائج أو قوالب متاحة",
                "recommendations": "إنشاء قوالب جديدة أو توسيع قاعدة البيانات"
            }

        explanation = {
            "selected_templates": [],
            "selection_criteria": {},
            "performance_analysis": {},
            "reasoning": "",
            "recommendations": []
        }

        # تحليل القوالب المختارة
        templates_by_source = {}
        confidence_scores = []
        total_templates = len(results)

        for result in results:
            source = result.get("source", "unknown")
            confidence = result.get("confidence", 0)
            template_id = result.get("template_id")

            if source not in templates_by_source:
                templates_by_source[source] = []
            templates_by_source[source].append(result)

            confidence_scores.append(confidence)

        # تحديد معايير الاختيار
        explanation["selection_criteria"] = {
            "total_templates_considered": total_templates,
            "sources_used": list(templates_by_source.keys()),
            "confidence_range": {
                "min": min(confidence_scores) if confidence_scores else 0,
                "max": max(confidence_scores) if confidence_scores else 0,
                "average": sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0
            },
            "quality_threshold": 0.7  # الحد الأدنى للجودة
        }

        # تحليل الأداء
        high_performing = [r for r in results if r.get("confidence", 0) >= 0.8]
        medium_performing = [r for r in results if 0.6 <= r.get("confidence", 0) < 0.8]
        low_performing = [r for r in results if r.get("confidence", 0) < 0.6]

        explanation["performance_analysis"] = {
            "high_performing": len(high_performing),
            "medium_performing": len(medium_performing),
            "low_performing": len(low_performing),
            "performance_distribution": {
                "excellent": f"{len(high_performing)} ({len(high_performing)/total_templates*100:.1f}%)",
                "good": f"{len(medium_performing)} ({len(medium_performing)/total_templates*100:.1f}%)",
                "needs_improvement": f"{len(low_performing)} ({len(low_performing)/total_templates*100:.1f}%)"
            }
        }

        # شرح عملية الاختيار
        reasoning_parts = []

        if templates_by_source.get("template"):
            reasoning_parts.append(f"تم اختيار {len(templates_by_source['template'])} قالب من قاعدة البيانات بناءً على درجات الأداء التاريخية")

        if templates_by_source.get("groq_ai"):
            reasoning_parts.append(f"تم توليد {len(templates_by_source['groq_ai'])} محتوى ديناميكي باستخدام الذكاء الاصطناعي")

        if templates_by_source.get("dynamic_generation"):
            reasoning_parts.append(f"تم إنشاء {len(templates_by_source['dynamic_generation'])} محتوى مخصص بناءً على تحليل البيانات")

        explanation["reasoning"] = ". ".join(reasoning_parts)

        # التوصيات
        avg_confidence = explanation["selection_criteria"]["confidence_range"]["average"]

        if avg_confidence < 0.7:
            explanation["recommendations"].append("تحسين جودة القوالب أو إنشاء قوالب جديدة")
        elif avg_confidence > 0.9:
            explanation["recommendations"].append("القوالب الحالية تعمل بشكل ممتاز - استمرار النهج الحالي")

        if len(high_performing) < total_templates * 0.3:
            explanation["recommendations"].append("زيادة عدد القوالب عالية الجودة")

        # تفاصيل القوالب المختارة
        for result in results[:5]:  # أول 5 قوالب فقط
            template_info = {
                "text_preview": result.get("text", "")[:100] + "..." if len(result.get("text", "")) > 100 else result.get("text", ""),
                "source": result.get("source", "unknown"),
                "confidence": result.get("confidence", 0),
                "template_id": result.get("template_id"),
                "selection_reason": self._get_template_selection_reason(result)
            }
            explanation["selected_templates"].append(template_info)

        return explanation

    def _get_template_selection_reason(self, result):
        """
        تحديد سبب اختيار قالب معين
        """
        source = result.get("source", "")
        confidence = result.get("confidence", 0)

        if source == "template":
            if confidence >= 0.9:
                return "قالب عالي الأداء مع سجل حافل بالنجاح"
            elif confidence >= 0.8:
                return "قالب مثبت الفعالية ومناسب للحملة"
            else:
                return "قالب أساسي متاح في قاعدة البيانات"
        elif source == "groq_ai":
            return "محتوى مولد بالذكاء الاصطناعي لضمان التنوع والإبداع"
        elif source == "dynamic_generation":
            return "محتوى مخصص بناءً على تحليل دقيق لبيانات الحملة"
        else:
            return "قالب تم اختياره بناءً على التوفر والتوافق الأساسي"

    def _explain_ai_generation(self, campaign_data):
        """
        شرح عملية توليد المحتوى بالذكاء الاصطناعي
        """
        explanation = {
            "ai_models_used": [],
            "generation_process": {},
            "prompt_engineering": {},
            "content_customization": {},
            "quality_assurance": {},
            "fallback_strategy": {}
        }

        # تحديد نماذج الذكاء الاصطناعي المستخدمة
        if settings.GROQ_API_KEY:
            explanation["ai_models_used"] = [
                "GROQ API - نماذج متقدمة (Llama 3.1, Llama 3.3, DeepSeek, Qwen)",
                "دعم للنماذج العربية مثل Allam-2-7B"
            ]
        else:
            explanation["ai_models_used"] = ["وضع تجريبي - محتوى ديناميكي بدون API خارجي"]

        # شرح عملية التوليد
        explanation["generation_process"] = {
            "steps": [
                "تحليل بيانات الحملة (الصناعة، الجمهور، الهدف)",
                "إنشاء prompt مخصص لنوع المحتوى المطلوب",
                "استدعاء نموذج الذكاء الاصطناعي المناسب",
                "معالجة وتنقيح النص المولد",
                "تقييم الجودة والتوافق"
            ],
            "languages_supported": ["العربية", "الإنجليزية", "مزيج عربي-إنجليزي"],
            "content_types": ["نصوص إعلانية", "منشورات وسائل التواصل", "عناوين بريد إلكتروني", "عناوين رئيسية"]
        }

        # هندسة الـ prompt
        explanation["prompt_engineering"] = {
            "optimization_techniques": [
                "تحديد السياق بوضوح (المنتج، الصناعة، الجمهور)",
                "تحديد النبرة المناسبة حسب الصناعة",
                "إضافة تعليمات محددة للإبداع والإقناع",
                "تحديد قيود الطول والتنسيق",
                "طلب عدة خيارات متنوعة"
            ],
            "contextual_variables": {
                "product_name": campaign_data.get("product_name", "غير محدد"),
                "industry": campaign_data.get("industry", "غير محدد"),
                "target_audience": campaign_data.get("target_audience", {}),
                "goal": campaign_data.get("goal", "غير محدد"),
                "keywords": campaign_data.get("keywords", [])
            },
            "quality_parameters": {
                "max_tokens": "200-300 كلمة",
                "temperature": "0.7 (توازن بين الإبداع والتركيز)",
                "creativity_level": "عالي مع الحفاظ على الاحترافية"
            }
        }

        # تخصيص المحتوى
        explanation["content_customization"] = {
            "personalization_factors": [
                "خصائص الجمهور المستهدف (العمر، الاهتمامات، الموقع)",
                "مستوى الميزانية ونوع المنتج",
                "الاعتبارات الثقافية واللغوية",
                "أهداف الحملة (وعي، تحويل، تفاعل)"
            ],
            "adaptation_strategies": [
                "تعديل النبرة حسب الفئة العمرية",
                "استخدام مصطلحات تقنية للصناعات المتخصصة",
                "إضافة لمسات ثقافية محلية",
                "تحسين للمنصات المختلفة"
            ],
            "localization_features": [
                "دعم كامل للغة العربية واللهجات المحلية",
                "مراعاة التقاليد والقيم الثقافية",
                "استخدام أمثلة ومراجع محلية"
            ]
        }

        # ضمان الجودة
        explanation["quality_assurance"] = {
            "validation_checks": [
                "التوافق مع إرشادات العلامة التجارية",
                "عدم وجود أخطاء إملائية أو نحوية",
                "التوافق مع النبرة المطلوبة",
                "القيمة الإعلانية والإقناع",
                "الالتزام بحدود الطول المحددة"
            ],
            "performance_metrics": [
                "درجة الإبداع والأصالة",
                "قوة الرسالة الإعلانية",
                "مدى التوافق مع الجمهور المستهدف",
                "إمكانية التحويل والفعالية"
            ],
            "improvement_mechanisms": [
                "تحليل تغذية المستخدمين الراجعة",
                "تحديث القوالب بناءً على الأداء",
                "تطوير مستمر لنماذج الذكاء الاصطناعي"
            ]
        }

        # استراتيجية الاحتياط
        explanation["fallback_strategy"] = {
            "primary_method": "توليد محتوى بالذكاء الاصطناعي",
            "backup_methods": [
                "استخدام قوالب من قاعدة البيانات",
                "توليد محتوى ديناميكي بناءً على القواعد",
                "إنشاء محتوى مخصص يدوياً"
            ],
            "failure_handling": [
                "إعادة المحاولة مع نماذج مختلفة",
                "تقليل تعقيد الطلب",
                "التبديل للوضع التجريبي",
                "إشعار المستخدم بضرورة المراجعة اليدوية"
            ],
            "reliability_measures": [
                "اختبار مستمر لواجهات API",
                "مراقبة أداء النماذج",
                "تحديث مفاتيح API تلقائياً",
                "نسخ احتياطي للقوالب الأساسية"
            ]
        }

        return explanation

    def _explain_ranking_criteria(self, results):
        """
        شرح معايير ترتيب النتائج
        """
        if not results:
            return {
                "ranking_criteria": "لا توجد نتائج للترتيب",
                "reasoning": "عدم وجود محتوى للتقييم",
                "recommendations": "إنشاء محتوى أو قوالب جديدة"
            }

        explanation = {
            "ranking_criteria": {},
            "scoring_factors": {},
            "performance_metrics": {},
            "reasoning": "",
            "recommendations": []
        }

        # معايير الترتيب الأساسية
        explanation["ranking_criteria"] = {
            "primary_factor": "درجة الثقة (Confidence Score)",
            "secondary_factors": [
                "مصدر المحتوى (قوالب، ذكاء اصطناعي، توليد ديناميكي)",
                "درجة الأداء التاريخية للقوالب",
                "مدى تخصيص المحتوى لبيانات الحملة",
                "جودة وأصالة النص"
            ],
            "sorting_method": "ترتيب تنازلي حسب درجة الثقة",
            "quality_thresholds": {
                "excellent": ">= 0.9",
                "good": "0.7 - 0.89",
                "acceptable": "0.5 - 0.69",
                "needs_review": "< 0.5"
            }
        }

        # عوامل التقييم
        total_results = len(results)
        confidence_scores = [r.get("confidence", 0) for r in results]

        explanation["scoring_factors"] = {
            "confidence_analysis": {
                "total_results": total_results,
                "average_confidence": round(sum(confidence_scores) / total_results, 3) if confidence_scores else 0,
                "confidence_range": {
                    "min": min(confidence_scores) if confidence_scores else 0,
                    "max": max(confidence_scores) if confidence_scores else 0,
                    "median": sorted(confidence_scores)[total_results // 2] if confidence_scores else 0
                },
                "distribution": self._analyze_confidence_distribution(confidence_scores)
            },
            "source_weighting": {
                "template": "0.8-1.0 (بناءً على الأداء التاريخي)",
                "groq_ai": "0.9 (ثقة عالية في المحتوى المولد)",
                "dynamic_generation": "0.8 (محتوى مخصص ومحسن)",
                "mock_content": "0.6 (محتوى تجريبي)"
            },
            "quality_indicators": [
                "التوافق مع النبرة المطلوبة",
                "استخدام الكلمات المفتاحية بشكل فعال",
                "قوة الرسالة الإعلانية",
                "الإبداع والأصالة",
                "التوافق مع الجمهور المستهدف"
            ]
        }

        # مقاييس الأداء
        high_quality = len([r for r in results if r.get("confidence", 0) >= 0.8])
        medium_quality = len([r for r in results if 0.6 <= r.get("confidence", 0) < 0.8])
        low_quality = len([r for r in results if r.get("confidence", 0) < 0.6])

        explanation["performance_metrics"] = {
            "quality_breakdown": {
                "high_quality": f"{high_quality} ({high_quality/total_results*100:.1f}%)",
                "medium_quality": f"{medium_quality} ({medium_quality/total_results*100:.1f}%)",
                "low_quality": f"{low_quality} ({low_quality/total_results*100:.1f}%)"
            },
            "ranking_stability": "مستقر - الترتيب يعتمد على مقاييس موضوعية",
            "diversity_score": self._calculate_diversity_score(results),
            "overall_effectiveness": self._calculate_overall_effectiveness(results)
        }

        # شرح منطق الترتيب
        reasoning_parts = []

        if high_quality > 0:
            reasoning_parts.append(f"تم تصنيف {high_quality} محتوى عالي الجودة في المقدمة")

        if medium_quality > 0:
            reasoning_parts.append(f"تم ترتيب {medium_quality} محتوى متوسط الجودة في الوسط")

        if low_quality > 0:
            reasoning_parts.append(f"تم وضع {low_quality} محتوى منخفض الجودة في النهاية للمراجعة")

        reasoning_parts.append("الترتيب يضمن أن أفضل المحتوى يظهر أولاً للمستخدم")
        reasoning_parts.append("يتم تحديث درجات الثقة بناءً على تفاعل المستخدمين")

        explanation["reasoning"] = ". ".join(reasoning_parts)

        # التوصيات
        avg_confidence = sum(confidence_scores) / total_results if confidence_scores else 0

        if avg_confidence < 0.7:
            explanation["recommendations"].append("تحسين جودة المحتوى أو إضافة قوالب أفضل")
        elif high_quality / total_results < 0.5:
            explanation["recommendations"].append("زيادة نسبة المحتوى عالي الجودة")
        else:
            explanation["recommendations"].append("الترتيب الحالي فعال ويعكس جودة المحتوى")

        return explanation

    def _analyze_confidence_distribution(self, confidence_scores):
        """
        تحليل توزيع درجات الثقة
        """
        if not confidence_scores:
            return {}

        distribution = {
            "excellent": len([s for s in confidence_scores if s >= 0.9]),
            "good": len([s for s in confidence_scores if 0.8 <= s < 0.9]),
            "fair": len([s for s in confidence_scores if 0.7 <= s < 0.8]),
            "poor": len([s for s in confidence_scores if s < 0.7])
        }

        total = len(confidence_scores)
        return {k: f"{v} ({v/total*100:.1f}%)" for k, v in distribution.items()}

    def _calculate_diversity_score(self, results):
        """
        حساب درجة تنوع المحتوى
        """
        if not results:
            return 0

        # تنوع المصادر
        sources = set(r.get("source", "") for r in results)
        source_diversity = len(sources) / 3  # 3 مصادر محتملة

        # تنوع الطول
        lengths = [len(r.get("text", "")) for r in results]
        if lengths:
            avg_length = sum(lengths) / len(lengths)
            length_variance = sum((l - avg_length) ** 2 for l in lengths) / len(lengths)
            length_diversity = min(length_variance / 1000, 1)  # تطبيع
        else:
            length_diversity = 0

        # تنوع المحتوى (تقدير بسيط)
        unique_content = len(set(r.get("text", "") for r in results))
        content_diversity = unique_content / len(results)

        overall_diversity = (source_diversity + length_diversity + content_diversity) / 3
        return round(overall_diversity * 100, 1)

    def _calculate_overall_effectiveness(self, results):
        """
        حساب الفعالية العامة للنتائج
        """
        if not results:
            return 0

        avg_confidence = sum(r.get("confidence", 0) for r in results) / len(results)
        diversity_score = self._calculate_diversity_score(results)

        # الفعالية = متوسط الثقة + تنوع × 0.2
        effectiveness = avg_confidence + (diversity_score / 100) * 0.2

        return round(min(effectiveness, 1.0) * 100, 1)

    def _generate_alternatives(self, campaign_data, results):
        """
        توليد بدائل متنوعة للمحتوى
        """
        alternatives = {
            "template_variations": [],
            "tone_alternatives": [],
            "length_variations": [],
            "platform_specific": [],
            "creative_approaches": [],
            "recommendations": []
        }

        if not results:
            alternatives["recommendations"] = ["إنشاء محتوى أساسي أولاً قبل توليد البدائل"]
            return alternatives

        # بدائل القوالب
        alternatives["template_variations"] = self._generate_template_alternatives(campaign_data, results)

        # بدائل النبرة
        alternatives["tone_alternatives"] = self._generate_tone_alternatives(campaign_data)

        # بدائل الطول
        alternatives["length_variations"] = self._generate_length_alternatives(results)

        # بدائل خاصة بالمنصات
        alternatives["platform_specific"] = self._generate_platform_alternatives(campaign_data, results)

        # نهج إبداعي مختلف
        alternatives["creative_approaches"] = self._generate_creative_approaches(campaign_data)

        # التوصيات العامة
        alternatives["recommendations"] = self._generate_alternatives_recommendations(campaign_data, results)

        return alternatives

    def _generate_template_alternatives(self, campaign_data, results):
        """
        توليد بدائل بناءً على قوالب مختلفة
        """
        alternatives = []

        # تحديد أنواع القوالب المتاحة
        template_types = ["ad_copy", "social_media_post", "email_subject", "headline"]

        for content_type in template_types:
            if content_type != campaign_data.get("content_type", "ad_copy"):
                alternatives.append({
                    "type": "نوع محتوى مختلف",
                    "content_type": content_type,
                    "description": f"تجربة {content_type} بدلاً من النوع الحالي",
                    "expected_benefit": "تنويع أشكال المحتوى لاختبار الاستجابة",
                    "implementation_effort": "منخفض"
                })

        # بدائل بناءً على درجة الثقة
        high_confidence = [r for r in results if r.get("confidence", 0) >= 0.8]
        low_confidence = [r for r in results if r.get("confidence", 0) < 0.6]

        if high_confidence:
            alternatives.append({
                "type": "تحسين القوالب عالية الأداء",
                "description": "تطوير القوالب الناجحة لإنتاج نسخ محسنة",
                "based_on": f"{len(high_confidence)} قالب ناجح",
                "expected_benefit": "تحسين مستمر للنتائج المثبتة",
                "implementation_effort": "متوسط"
            })

        if low_confidence:
            alternatives.append({
                "type": "إعادة تصميم القوالب الضعيفة",
                "description": "مراجعة وتحسين القوالب منخفضة الأداء",
                "based_on": f"{len(low_confidence)} قالب يحتاج تحسين",
                "expected_benefit": "رفع مستوى الجودة العام",
                "implementation_effort": "عالي"
            })

        return alternatives

    def _generate_tone_alternatives(self, campaign_data):
        """
        توليد بدائل بناءً على نبرة مختلفة
        """
        industry = campaign_data.get("industry", "").lower()
        current_tone = self._determine_content_tone(campaign_data)

        alternatives = []

        # خريطة النبرات البديلة
        tone_alternatives = {
            "technology": ["مبتكر وتقني", "بسيط وسهل", "متقدم ومعقد", "تعليمي وإرشادي"],
            "fashion": ["أنيق وعصري", "جريء ومميز", "كلاسيكي وأنيق", "شبابي ومبهج"],
            "food": ["شهي وجذاب", "صحي ومغذي", "سريع ومريح", "تقليدي وأصيل"],
            "health": ["صحي وموثوق", "وقائي وتوعوي", "علاجي وفعال", "طبيعي وعضوي"],
            "education": ["تعليمي ومفيد", "تفاعلي ومشوق", "أكاديمي وعميق", "عملي وتطبيقي"],
            "finance": ["مهني وموثوق", "بسيط وواضح", "استثماري ومربح", "آمن ومضمون"]
        }

        available_tones = tone_alternatives.get(industry, ["محايد وجذاب", "رسمي ومهني", "ودي ومقرب"])

        for tone in available_tones:
            if tone != current_tone:
                alternatives.append({
                    "type": "نبرة مختلفة",
                    "tone": tone,
                    "description": f"استخدام نبرة {tone}",
                    "expected_benefit": "جذب شرائح مختلفة من الجمهور",
                    "implementation_effort": "منخفض"
                })

        return alternatives

    def _generate_length_alternatives(self, results):
        """
        توليد بدائل بناءً على طول مختلف
        """
        alternatives = []

        if not results:
            return alternatives

        # تحليل الأطوال الحالية
        lengths = [len(r.get("text", "")) for r in results]
        avg_length = sum(lengths) / len(lengths) if lengths else 0

        # بدائل الطول
        length_options = [
            {
                "name": "قصير جداً",
                "range": "10-30 كلمة",
                "use_case": "منشورات سريعة، عناوين، إعلانات قصيرة",
                "expected_benefit": "سهولة القراءة والفهم السريع"
            },
            {
                "name": "متوسط",
                "range": "30-80 كلمة",
                "use_case": "منشورات مفصلة، وصف المنتجات",
                "expected_benefit": "توازن بين الإيجاز والتفاصيل"
            },
            {
                "name": "طويل",
                "range": "80-150 كلمة",
                "use_case": "مقالات، قصص، محتوى تفاعلي",
                "expected_benefit": "بناء علاقة أعمق مع الجمهور"
            }
        ]

        current_category = "متوسط"
        if avg_length < 30:
            current_category = "قصير جداً"
        elif avg_length > 80:
            current_category = "طويل"

        for option in length_options:
            if option["name"] != current_category:
                alternatives.append({
                    "type": "طول مختلف",
                    "length_category": option["name"],
                    "range": option["range"],
                    "use_case": option["use_case"],
                    "expected_benefit": option["expected_benefit"],
                    "implementation_effort": "منخفض"
                })

        return alternatives

    def _generate_platform_alternatives(self, campaign_data, results):
        """
        توليد بدائل خاصة بالمنصات
        """
        platforms = campaign_data.get("platforms", ["general"])
        alternatives = []

        # منصات بديلة
        platform_suggestions = {
            "facebook": ["instagram", "twitter", "linkedin", "tiktok"],
            "instagram": ["facebook", "tiktok", "pinterest", "snapchat"],
            "twitter": ["facebook", "linkedin", "instagram", "threads"],
            "linkedin": ["facebook", "twitter", "instagram", "youtube"],
            "tiktok": ["instagram", "youtube", "snapchat", "facebook"],
            "general": ["facebook", "instagram", "twitter", "linkedin", "youtube"]
        }

        for platform in platforms:
            suggested = platform_suggestions.get(platform, ["facebook", "instagram"])
            for alt_platform in suggested[:3]:  # أول 3 بدائل
                alternatives.append({
                    "type": "منصة بديلة",
                    "current_platform": platform,
                    "suggested_platform": alt_platform,
                    "description": f"تخصيص المحتوى لمنصة {alt_platform}",
                    "expected_benefit": "تحسين الأداء على المنصات المختلفة",
                    "implementation_effort": "متوسط"
                })

        return alternatives

    def _generate_creative_approaches(self, campaign_data):
        """
        توليد نهج إبداعي مختلف
        """
        alternatives = []

        goal = campaign_data.get("goal", "").lower()
        industry = campaign_data.get("industry", "").lower()

        creative_approaches = [
            {
                "name": "القصة والسرد",
                "description": "استخدام تقنية السرد القصصي لجذب الانتباه",
                "best_for": ["awareness", "brand"],
                "expected_benefit": "زيادة التفاعل والتذكر"
            },
            {
                "name": "الأسئلة والتفاعل",
                "description": "طرح أسئلة لإثارة تفكير الجمهور",
                "best_for": ["engagement", "education"],
                "expected_benefit": "تشجيع التفاعل والمشاركة"
            },
            {
                "name": "الإثبات الاجتماعي",
                "description": "استخدام تقييمات وشهادات العملاء",
                "best_for": ["conversion", "trust"],
                "expected_benefit": "بناء الثقة والمصداقية"
            },
            {
                "name": "العروض والحوافز",
                "description": "التركيز على العروض والمزايا الخاصة",
                "best_for": ["sales", "conversion"],
                "expected_benefit": "زيادة معدلات التحويل"
            },
            {
                "name": "التعليم والقيمة",
                "description": "تقديم معلومات مفيدة وقيمة للجمهور",
                "best_for": ["education", "awareness"],
                "expected_benefit": "بناء السلطة والخبرة"
            }
        ]

        for approach in creative_approaches:
            if goal in approach["best_for"] or industry in approach["best_for"]:
                alternatives.append({
                    "type": "نهج إبداعي",
                    "approach_name": approach["name"],
                    "description": approach["description"],
                    "expected_benefit": approach["expected_benefit"],
                    "implementation_effort": "متوسط"
                })

        return alternatives

    def _generate_alternatives_recommendations(self, campaign_data, results):
        """
        توليد توصيات عامة للبدائل
        """
        recommendations = []

        # تحليل الحالة الحالية
        if len(results) < 3:
            recommendations.append("زيادة عدد النتائج للحصول على بدائل أكثر تنوعاً")

        # تحليل الجودة
        avg_confidence = sum(r.get("confidence", 0) for r in results) / len(results) if results else 0
        if avg_confidence < 0.7:
            recommendations.append("تحسين جودة المحتوى الأساسي قبل تجربة البدائل")

        # تحليل التنوع
        sources = set(r.get("source", "") for r in results)
        if len(sources) < 2:
            recommendations.append("استخدام مصادر متنوعة للمحتوى (قوالب، ذكاء اصطناعي، توليد ديناميكي)")

        # توصيات بناءً على البيانات
        if campaign_data.get("budget", 0) > 10000:
            recommendations.append("تجربة بدائل متقدمة مع ميزانية أكبر للاختبار")

        if campaign_data.get("target_audience", {}).get("age_range"):
            age_range = campaign_data["target_audience"]["age_range"]
            if len(age_range) == 2 and age_range[1] - age_range[0] > 30:
                recommendations.append("تجربة بدائل مختلفة لتغطية الفئات العمرية المتنوعة")

        recommendations.extend([
            "اختبار البدائل في حملات تجريبية صغيرة أولاً",
            "قياس أداء كل بديل وتحليل النتائج",
            "الحفاظ على اتساق العلامة التجارية عبر جميع البدائل"
        ])

        return recommendations

    def _generate_recommendations(self, campaign_data, results):
        """
        توليد توصيات قابلة للتنفيذ بناءً على أداء الحملة
        """
        recommendations = {
            "immediate_actions": [],
            "short_term_optimizations": [],
            "long_term_strategies": [],
            "performance_targets": {},
            "monitoring_suggestions": [],
            "budget_optimizations": []
        }

        if not results:
            recommendations["immediate_actions"] = ["إنشاء محتوى أساسي للحملة"]
            return recommendations

        # تحليل البيانات لتوليد التوصيات
        analysis_data = {
            "campaign_analysis": self._analyze_input_data(campaign_data),
            "confidence_analysis": self._analyze_confidence_factors(results),
            "template_analysis": self._explain_template_selection(results),
            "ranking_analysis": self._explain_ranking_criteria(results)
        }

        # إجراءات فورية
        recommendations["immediate_actions"] = self._generate_immediate_actions(campaign_data, results, analysis_data)

        # تحسينات قصيرة الأمد
        recommendations["short_term_optimizations"] = self._generate_short_term_optimizations(campaign_data, results, analysis_data)

        # استراتيجيات طويلة الأمد
        recommendations["long_term_strategies"] = self._generate_long_term_strategies(campaign_data, results, analysis_data)

        # أهداف الأداء
        recommendations["performance_targets"] = self._set_performance_targets(results, analysis_data)

        # اقتراحات المراقبة
        recommendations["monitoring_suggestions"] = self._generate_monitoring_suggestions(campaign_data, results)

        # تحسينات الميزانية
        recommendations["budget_optimizations"] = self._generate_budget_optimizations(campaign_data, results, analysis_data)

        return recommendations

    def _generate_immediate_actions(self, campaign_data, results, analysis_data):
        """
        توليد إجراءات فورية
        """
        actions = []

        # تحليل البيانات الناقصة
        campaign_analysis = analysis_data["campaign_analysis"]
        data_completeness = campaign_analysis["campaign_summary"].get("data_completeness", 0)

        if data_completeness < 70:
            actions.append({
                "action": "استكمال بيانات الحملة",
                "priority": "عالية",
                "description": f"اكتمال البيانات الحالي: {data_completeness:.1f}%",
                "expected_impact": "تحسين دقة توليد المحتوى بنسبة 30-50%",
                "timeframe": "1-2 أيام"
            })

        # تحليل جودة المحتوى
        confidence_analysis = analysis_data["confidence_analysis"]
        overall_confidence = confidence_analysis.get("overall_confidence", 0)

        if overall_confidence < 0.7:
            actions.append({
                "action": "مراجعة وتحسين المحتوى المولد",
                "priority": "عالية",
                "description": f"متوسط الثقة الحالي: {overall_confidence:.2f}",
                "expected_impact": "رفع جودة المحتوى بنسبة 20-40%",
                "timeframe": "2-3 أيام"
            })

        # تحليل المخاطر
        risk_assessment = confidence_analysis.get("risk_assessment", {})
        overall_risk = risk_assessment.get("overall_risk_level", "منخفض")

        if "عالية" in overall_risk or "متوسطة" in overall_risk:
            actions.append({
                "action": "تقييم وتخفيف المخاطر",
                "priority": "عالية",
                "description": f"مستوى المخاطر: {overall_risk}",
                "expected_impact": "تقليل المخاطر المحتملة",
                "timeframe": "3-5 أيام"
            })

        # تحسينات سريعة
        actions.extend([
            {
                "action": "اختبار A/B للمحتوى الأفضل أداءً",
                "priority": "متوسطة",
                "description": "اختبار نسخ مختلفة من المحتوى",
                "expected_impact": "تحديد أفضل النسخ أداءً",
                "timeframe": "1 أسبوع"
            },
            {
                "action": "تحليل المنافسين والاتجاهات",
                "priority": "متوسطة",
                "description": "دراسة حملات المنافسين الناجحة",
                "expected_impact": "تحسين الاستراتيجية العامة",
                "timeframe": "3-5 أيام"
            }
        ])

        return actions

    def _generate_short_term_optimizations(self, campaign_data, results, analysis_data):
        """
        توليد تحسينات قصيرة الأمد
        """
        optimizations = []

        # تحسينات بناءً على تحليل القوالب
        template_analysis = analysis_data["template_analysis"]
        performance_analysis = template_analysis.get("performance_analysis", {})

        high_performing = performance_analysis.get("high_performing", 0)
        total_templates = len(results)

        if high_performing / total_templates < 0.5 and total_templates > 0:
            optimizations.append({
                "optimization": "تحسين القوالب منخفضة الأداء",
                "category": "محتوى",
                "description": f"تحسين {total_templates - high_performing} قالب منخفض الأداء",
                "expected_impact": "رفع متوسط الأداء بنسبة 25%",
                "timeframe": "1-2 أسابيع",
                "resources_needed": "محرر محتوى، أدوات تحليل"
            })

        # تحسينات بناءً على الجمهور المستهدف
        target_audience = campaign_data.get("target_audience", {})
        if not target_audience.get("interests"):
            optimizations.append({
                "optimization": "تطوير فهم أعمق للجمهور المستهدف",
                "category": "جمهور",
                "description": "إجراء بحوث جمهور لتحديد الاهتمامات والسلوكيات",
                "expected_impact": "تحسين دقة الاستهداف بنسبة 40%",
                "timeframe": "2-3 أسابيع",
                "resources_needed": "بحوث سوق، استطلاعات"
            })

        # تحسينات تقنية
        optimizations.extend([
            {
                "optimization": "تحسين استخدام الذكاء الاصطناعي",
                "category": "تقنية",
                "description": "تدريب النماذج وتحسين الـ prompts",
                "expected_impact": "تحسين جودة المحتوى المولد",
                "timeframe": "2-4 أسابيع",
                "resources_needed": "مهندس ذكاء اصطناعي، بيانات تدريب"
            },
            {
                "optimization": "توسيع قاعدة القوالب",
                "category": "محتوى",
                "description": "إضافة قوالب جديدة متنوعة",
                "expected_impact": "زيادة الخيارات المتاحة للمحتوى",
                "timeframe": "2-3 أسابيع",
                "resources_needed": "كاتب محتوى، مصمم قوالب"
            }
        ])

        return optimizations

    def _generate_long_term_strategies(self, campaign_data, results, analysis_data):
        """
        توليد استراتيجيات طويلة الأمد
        """
        strategies = []

        # استراتيجيات بناءً على الصناعة
        industry = campaign_data.get("industry", "")
        if industry.lower() in ["technology", "finance", "health"]:
            strategies.append({
                "strategy": "بناء نظام ذكاء اصطناعي متخصص",
                "category": "تقنية",
                "description": f"تطوير نماذج ذكاء اصطناعي متخصصة في {industry}",
                "expected_impact": "تحسين دقة المحتوى بنسبة 60%",
                "timeframe": "3-6 أشهر",
                "investment_needed": "عالي",
                "success_metrics": ["دقة المحتوى", "رضا العملاء", "معدل التحويل"]
            })

        # استراتيجيات البيانات
        strategies.append({
            "strategy": "بناء قاعدة بيانات شاملة للأداء",
            "category": "بيانات",
            "description": "جمع وتحليل بيانات أداء الحملات التاريخية",
            "expected_impact": "تحسين دقة التنبؤات والتوصيات",
            "timeframe": "6-12 شهر",
            "investment_needed": "متوسط",
            "success_metrics": ["دقة التنبؤ", "تحسن الأداء", "كفاءة الميزانية"]
        })

        # استراتيجيات التوسع
        budget = campaign_data.get("budget", 0)
        if budget > 50000:
            strategies.append({
                "strategy": "التوسع في الأسواق الجديدة",
                "category": "نمو",
                "description": "تطوير استراتيجيات للدخول في أسواق جديدة",
                "expected_impact": "زيادة حجم السوق المستهدف",
                "timeframe": "6-18 شهر",
                "investment_needed": "عالي",
                "success_metrics": ["حصة السوق", "إيرادات جديدة", "قاعدة عملاء"]
            })

        # استراتيجيات الابتكار
        strategies.extend([
            {
                "strategy": "تطوير منتجات جديدة للمحتوى",
                "category": "ابتكار",
                "description": "إنشاء أدوات ومنتجات جديدة لإنتاج المحتوى",
                "expected_impact": "تنويع مصادر الإيرادات",
                "timeframe": "6-12 شهر",
                "investment_needed": "متوسط",
                "success_metrics": ["منتجات جديدة", "إيرادات إضافية", "رضا العملاء"]
            },
            {
                "strategy": "بناء شراكات استراتيجية",
                "category": "أعمال",
                "description": "تكوين شراكات مع منصات وشركات أخرى",
                "expected_impact": "توسيع الوصول والقدرات",
                "timeframe": "3-9 أشهر",
                "investment_needed": "منخفض",
                "success_metrics": ["عدد الشراكات", "زيادة المستخدمين", "تحسن الخدمات"]
            }
        ])

        return strategies

    def _set_performance_targets(self, results, analysis_data):
        """
        تحديد أهداف الأداء
        """
        current_confidence = analysis_data["confidence_analysis"].get("overall_confidence", 0)

        targets = {
            "short_term": {
                "target_confidence": min(current_confidence + 0.1, 0.9),
                "target_period": "3 أشهر",
                "key_metrics": [
                    f"رفع متوسط الثقة إلى {min(current_confidence + 0.1, 0.9):.2f}",
                    "تقليل المحتوى منخفض الجودة بنسبة 30%",
                    "زيادة نسبة القوالب عالية الأداء إلى 70%"
                ]
            },
            "medium_term": {
                "target_confidence": min(current_confidence + 0.2, 0.95),
                "target_period": "6 أشهر",
                "key_metrics": [
                    f"تحقيق متوسط ثقة {min(current_confidence + 0.2, 0.95):.2f}",
                    "تطوير 50% من القوالب الجديدة",
                    "تحسين دقة الاستهداف بنسبة 40%"
                ]
            },
            "long_term": {
                "target_confidence": 0.95,
                "target_period": "12 شهر",
                "key_metrics": [
                    "الوصول لمتوسط ثقة 0.95",
                    "بناء نظام ذكاء اصطناعي متطور",
                    "تحقيق معدل نجاح 90% في الحملات"
                ]
            }
        }

        return targets

    def _generate_monitoring_suggestions(self, campaign_data, results):
        """
        توليد اقتراحات المراقبة
        """
        suggestions = [
            {
                "metric": "أداء المحتوى",
                "monitoring_frequency": "يومي",
                "tools": ["Google Analytics", "Facebook Insights", "Twitter Analytics"],
                "kpis": ["معدل النقر", "معدل التحويل", "معدل التفاعل"]
            },
            {
                "metric": "رضا العملاء",
                "monitoring_frequency": "أسبوعي",
                "tools": ["استطلاعات", "تغذية راجعة", "تقييمات"],
                "kpis": ["درجة الرضا", "ملاحظات العملاء", "معدل الاحتفاظ"]
            },
            {
                "metric": "كفاءة الميزانية",
                "monitoring_frequency": "أسبوعي",
                "tools": ["تقارير الميزانية", "تتبع التكاليف"],
                "kpis": ["تكلفة لكل عميل", "عائد الاستثمار", "كفاءة الإنفاق"]
            },
            {
                "metric": "جودة المحتوى",
                "monitoring_frequency": "أسبوعي",
                "tools": ["أدوات تحليل المحتوى", "تقييمات داخلية"],
                "kpis": ["متوسط درجة الثقة", "نسبة القبول", "معدل التحسين"]
            }
        ]

        return suggestions

    def _generate_budget_optimizations(self, campaign_data, results, analysis_data):
        """
        توليد تحسينات الميزانية
        """
        budget = campaign_data.get("budget", 0)
        platforms = campaign_data.get("platforms", [])

        optimizations = []

        if budget > 0:
            # تحليل التوزيع الحالي
            current_allocation = budget / len(platforms) if platforms else budget

            optimizations.append({
                "optimization": "تحسين توزيع الميزانية",
                "current_allocation": f"{current_allocation:.0f} دولار لكل منصة",
                "suggested_allocation": "بناءً على الأداء التاريخي",
                "expected_savings": "15-25%",
                "implementation": "إعادة توزيع بناءً على بيانات الأداء"
            })

        # تحسينات بناءً على الأداء
        confidence_analysis = analysis_data["confidence_analysis"]
        overall_confidence = confidence_analysis.get("overall_confidence", 0)

        if overall_confidence > 0.8:
            optimizations.append({
                "optimization": "زيادة الاستثمار في القنوات عالية الأداء",
                "rationale": "المحتوى الحالي يحقق نتائج ممتازة",
                "expected_roi": "تحسن بنسبة 30-50%",
                "implementation": "زيادة الميزانية لأفضل القنوات"
            })
        elif overall_confidence < 0.6:
            optimizations.append({
                "optimization": "تقليل المخاطر المالية",
                "rationale": "جودة المحتوى تحتاج تحسين",
                "expected_savings": "20-30%",
                "implementation": "تقليل الإنفاق حتى تحسين الجودة"
            })

        return optimizations

    def explain_content_generation(self, campaign_data, results):
        explanation = {
            "decision_process": {
                "input_analysis": self._analyze_input_data(campaign_data),
                "template_selection": self._explain_template_selection(results),
                "ai_generation": self._explain_ai_generation(campaign_data),
                "ranking_criteria": self._explain_ranking_criteria(results)
            },
            "alternatives": self._generate_alternatives(campaign_data, results),
            "confidence_factors": self._analyze_confidence_factors(results),
            "recommendations": self._generate_recommendations(campaign_data, results)
        }
        return explanation
