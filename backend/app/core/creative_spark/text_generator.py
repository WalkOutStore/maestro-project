from typing import Dict, Any, List, Optional
import requests
import json
import os
from sqlalchemy.orm import Session

from app.models.knowledge_base import ContentTemplate
from app.config import settings


class TextGenerator:
    """
    مولد النصوص الإعلانية باستخدام نماذج اللغة
    """
    
    def __init__(self, db: Session = None):
        """
        تهيئة مولد النصوص
        """
        self.db = db
        self.templates = {}
        self._load_templates()
    
    def _load_templates(self) -> None:
        """
        تحميل قوالب المحتوى من قاعدة البيانات
        """
        if self.db:
            templates = self.db.query(ContentTemplate).filter(ContentTemplate.content_type == "text").all()
            for template in templates:
                if template.name not in self.templates:
                    self.templates[template.name] = []
                
                self.templates[template.name].append({
                    "id": template.id,
                    "template_data": template.template_data,
                    "variables": template.variables,
                    "performance_score": template.performance_score
                })
    
    def generate_ad_copy(self, campaign_data: Dict[str, Any], content_type: str = "ad_copy") -> List[Dict[str, Any]]:
        """
        توليد نص إعلاني بناءً على بيانات الحملة
        """
        results = []
        
        # استخدام القوالب إذا كانت متاحة
        if content_type in self.templates:
            templates = self.templates[content_type]
            for template in templates:
                try:
                    # استبدال المتغيرات في القالب
                    text = template["template_data"]
                    for var_name, var_key in template["variables"].items():
                        if var_key in campaign_data:
                            text = text.replace(f"{{{{{var_name}}}}}", str(campaign_data[var_key]))
                    
                    results.append({
                        "text": text,
                        "source": "template",
                        "template_id": template["id"],
                        "confidence": template["performance_score"] / 10.0  # تحويل الدرجة إلى قيمة بين 0 و 1
                    })
                except Exception as e:
                    print(f"Error applying template {template['id']}: {e}")
        
        # استخدام نموذج اللغة إذا كان مفتاح API متاحًا
        if settings.OPENAI_API_KEY:
            try:
                # توليد نص باستخدام OpenAI API
                generated_texts = self._generate_with_openai(campaign_data, content_type)
                for text in generated_texts:
                    results.append({
                        "text": text,
                        "source": "openai",
                        "template_id": None,
                        "confidence": 0.8  # قيمة افتراضية
                    })
            except Exception as e:
                print(f"Error generating text with OpenAI: {e}")
        
        # ترتيب النتائج حسب الثقة
        results.sort(key=lambda x: x["confidence"], reverse=True)
        
        return results
    
    def _generate_with_openai(self, campaign_data: Dict[str, Any], content_type: str) -> List[str]:
        """
        توليد نص باستخدام OpenAI API
        """
        # هذه الدالة تحتاج إلى مفتاح API من OpenAI
        # سنترك التنفيذ فارغًا هنا ليتم ملؤه لاحقًا
        
        # مثال على كيفية استخدام OpenAI API
        """
        api_key = settings.OPENAI_API_KEY
        
        # إعداد الطلب
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        # إعداد محتوى الطلب
        prompt = self._create_prompt(campaign_data, content_type)
        data = {
            "model": "gpt-4",
            "messages": [
                {"role": "system", "content": "You are a creative marketing copywriter."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 200,
            "n": 3  # عدد النصوص المطلوب توليدها
        }
        
        # إرسال الطلب
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            data=json.dumps(data)
        )
        
        # معالجة الاستجابة
        if response.status_code == 200:
            result = response.json()
            texts = [choice["message"]["content"].strip() for choice in result["choices"]]
            return texts
        else:
            print(f"Error from OpenAI API: {response.status_code}, {response.text}")
            return []
        """
        
        # نعيد قائمة فارغة حتى يتم تنفيذ الدالة لاحقًا
        return []
    
    def _create_prompt(self, campaign_data: Dict[str, Any], content_type: str) -> str:
        """
        إنشاء نص توجيهي لنموذج اللغة
        """
        if content_type == "ad_copy":
            prompt = f"Write 3 compelling ad copies for a {campaign_data.get('industry', 'business')} "
            prompt += f"targeting {campaign_data.get('target_audience', 'customers')}. "
            prompt += f"The product/service is: {campaign_data.get('product_description', 'not specified')}. "
            prompt += f"Key benefits: {campaign_data.get('benefits', 'not specified')}. "
            prompt += f"Tone: {campaign_data.get('tone', 'professional')}. "
            prompt += "Each ad copy should have a headline and body text. "
            prompt += "Format each ad copy as: Headline: [headline]\nBody: [body]"
        
        elif content_type == "social_media_post":
            prompt = f"Write 3 engaging social media posts for {campaign_data.get('platform', 'social media')} "
            prompt += f"about {campaign_data.get('product_description', 'a product/service')}. "
            prompt += f"Target audience: {campaign_data.get('target_audience', 'customers')}. "
            prompt += f"Include relevant hashtags for {campaign_data.get('platform', 'social media')}."
        
        elif content_type == "email_subject":
            prompt = f"Write 3 attention-grabbing email subject lines for a {campaign_data.get('industry', 'business')} "
            prompt += f"promoting {campaign_data.get('product_description', 'a product/service')}. "
            prompt += f"The email is for {campaign_data.get('email_purpose', 'marketing')} purposes."
        
        else:
            prompt = f"Write marketing content of type {content_type} for a {campaign_data.get('industry', 'business')} "
            prompt += f"about {campaign_data.get('product_description', 'a product/service')}."
        
        return prompt
    
    def save_template(self, template_data: Dict[str, Any]) -> Optional[ContentTemplate]:
        """
        حفظ قالب محتوى جديد
        """
        if self.db:
            template = ContentTemplate(
                name=template_data["name"],
                description=template_data.get("description"),
                content_type=template_data["content_type"],
                template_data=template_data["template_data"],
                variables=template_data["variables"],
                performance_score=template_data.get("performance_score", 0.0)
            )
            self.db.add(template)
            self.db.commit()
            self.db.refresh(template)
            
            # تحديث الذاكرة المؤقتة
            if template.name not in self.templates:
                self.templates[template.name] = []
            
            self.templates[template.name].append({
                "id": template.id,
                "template_data": template.template_data,
                "variables": template.variables,
                "performance_score": template.performance_score
            })
            
            return template
        
        return None
    
    def update_template_performance(self, template_id: int, performance_score: float) -> bool:
        """
        تحديث درجة أداء القالب
        """
        if self.db:
            template = self.db.query(ContentTemplate).filter(ContentTemplate.id == template_id).first()
            if template:
                template.performance_score = performance_score
                self.db.commit()
                
                # تحديث الذاكرة المؤقتة
                for templates in self.templates.values():
                    for t in templates:
                        if t["id"] == template_id:
                            t["performance_score"] = performance_score
                            break
                
                return True
        
        return False
