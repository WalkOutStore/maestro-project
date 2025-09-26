from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from app.models.knowledge_base import ContentTemplate
from app.config import settings
from app.core.creative_spark.api_integrations import api_integrations

class TextGenerator:
    """
    مولد النصوص الإعلانية والمحتوى التسويقي بدون أي بيانات افتراضية.
    يعتمد فقط على القوالب الفعلية من قاعدة البيانات أو محتوى GROQ API.
    """

    def __init__(self, db: Session = None):
        self.db = db
        self.templates: Dict[str, List[Dict[str, Any]]] = {}
        self._load_templates()

    def _load_templates(self) -> None:
        """
        تحميل قوالب المحتوى الحقيقية من قاعدة البيانات.
        """
        if self.db:
            templates = self.db.query(ContentTemplate).all()
            for template in templates:
                if template.content_type not in self.templates:
                    self.templates[template.content_type] = []
                self.templates[template.content_type].append({
                    "id": template.id,
                    "template_data": template.template_data,
                    "variables": template.variables,
                    "performance_score": template.performance_score
                })

    def generate_ad_copy(self, campaign_data: Dict[str, Any], content_type: str = "ad_copy") -> List[Dict[str, Any]]:
        """
        توليد نص إعلاني ديناميكي باستخدام القوالب الفعلية أو GROQ API.
        """
        results: List[Dict[str, Any]] = []

        # استخدام القوالب الفعلية
        if content_type in self.templates:
            templates = self.templates[content_type]
            for template in templates:
                try:
                    text = template["template_data"]
                    for var_name, var_key in template["variables"].items():
                        if var_key in campaign_data:
                            text = text.replace(f"{{{{{var_name}}}}}", str(campaign_data[var_key]))
                    results.append({
                        "text": text,
                        "source": "template",
                        "template_id": template["id"],
                        "confidence": template["performance_score"] / 10.0
                    })
                except Exception as e:
                    print(f"Error applying template {template['id']}: {e}")

        # توليد نصوص ديناميكية باستخدام GROQ API
        if settings.GROQ_API_KEY:
            try:
                generated_texts = self._generate_dynamic_content(campaign_data, content_type)
                for text in generated_texts:
                    results.append({
                        "text": text,
                        "source": "groq_ai",
                        "template_id": None,
                        "confidence": 0.9
                    })
            except Exception as e:
                print(f"Error generating dynamic content with Groq: {e}")

        # ترتيب النتائج حسب الثقة
        results.sort(key=lambda x: x["confidence"], reverse=True)
        return results

    def _generate_dynamic_content(self, campaign_data: Dict[str, Any], content_type: str) -> List[str]:
        """
        توليد محتوى ديناميكي باستخدام GROQ API.
        """
        prompt = self._create_prompt(campaign_data, content_type)
        result = api_integrations.generate_text_with_groq(prompt, max_tokens=200)
        if result.get("success"):
            text = result["data"]["text"].strip()
            texts = [t.strip() for t in text.split('\n') if t.strip()]
            return texts[:3]
        else:
            print(f"Error generating dynamic content with Groq: {result.get('error')}")
            return []

    def _create_prompt(self, campaign_data: Dict[str, Any], content_type: str) -> str:
        """
        إنشاء نص توجيهي محسّن لنموذج اللغة.
        """
        industry = campaign_data.get('industry', 'الأعمال')
        product = campaign_data.get('product', 'المنتج')
        target_audience = campaign_data.get('target_audience', 'العملاء المحتملين')
        budget = campaign_data.get('budget', 0)
        goal = campaign_data.get('goal', 'زيادة المبيعات')

        if content_type == "ad_copy":
            prompt = (
                f"أنت خبير تسويقي محترف. اكتب 3 نصوص إعلانية جذابة باللغة العربية للمنتج التالي:\n"
                f"المنتج: {product}\nالصناعة: {industry}\nالجمهور المستهدف: {target_audience}\n"
                f"الميزانية: {budget} دولار\nالهدف: {goal}\n"
                "المتطلبات:\n- كل نص قصير ومؤثر (لا يزيد عن 50 كلمة)\n"
                "- استخدم لغة إقناعية وعاطفية\n- ركز على الفوائد والحلول\n"
                "- اجعل كل نص فريدًا ومتنوعًا\nاكتب كل نص في سطر منفصل."
            )
        elif content_type == "social_media_post":
            prompt = (
                f"أنت مدير وسائل تواصل اجتماعي محترف. اكتب 3 منشورات جذابة باللغة العربية:\n"
                f"المنتج: {product}\nالصناعة: {industry}\nالجمهور المستهدف: {target_audience}\n"
                "المتطلبات:\n- كل منشور مشوق ويحفز التفاعل\n- استخدم الرموز التعبيرية والهاشتاجات\n"
                "- اجعل المحتوى قابل للمشاركة والتعليق\nاكتب كل منشور في سطر منفصل."
            )
        elif content_type == "email_subject":
            prompt = (
                f"أنت خبير كتابة عناوين البريد الإلكتروني. اكتب 3 عناوين جذابة باللغة العربية:\n"
                f"المنتج: {product}\nالصناعة: {industry}\nالهدف: {goal}\n"
                "المتطلبات:\n- كل عنوان قصير (لا يزيد عن 10 كلمات)\n- يجب أن يثير الفضول\n"
                "- استخدم كلمات قوية ومؤثرة\nاكتب كل عنوان في سطر منفصل."
            )
        else:
            prompt = (
                f"أنت كاتب محتوى تسويقي محترف. اكتب محتوى {content_type} باللغة العربية للمنتج التالي:\n"
                f"المنتج: {product}\nالصناعة: {industry}\nالجمهور المستهدف: {target_audience}\n"
                "اكتب المحتوى بشكل جذاب ومقنع."
            )
        return prompt

    # طرق إضافية لتوليد أنواع مختلفة من المحتوى
    def generate_social_media_post(self, campaign_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        return self.generate_ad_copy(campaign_data, "social_media_post")

    def generate_email_subject(self, campaign_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        return self.generate_ad_copy(campaign_data, "email_subject")

    def generate_headline(self, campaign_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        return self.generate_ad_copy(campaign_data, "headline")
