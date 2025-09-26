from typing import Dict, Any, List, Optional
import os
import json
import time
from datetime import datetime, timedelta
import requests
from requests.exceptions import RequestException
from pytrends.request import TrendReq

try:
    import groq
    from groq import Groq
except ImportError:
    groq = None
    Groq = None
from app.config import settings


class APIIntegrations:
    """
    خدمة التكامل مع الـ APIs الخارجية
    """

    def __init__(self):
        """
        تهيئة خدمة التكامل مع الـ APIs
        """
        self._setup_apis()

    def _setup_apis(self) -> None:
        """
        إعداد الـ APIs المختلفة
        """
        # إعداد Google Trends API
        self.pytrends = None
        try:
            self.pytrends = TrendReq(hl='ar', tz=360)
            print("✅ Google Trends API configured successfully")
        except Exception as e:
            print(f"❌ Error setting up Google Trends API: {e}")



        # إعداد Google Gemini API
        
        # إعداد GROQ API
        if settings.GROQ_API_KEY:
            try:
                if Groq is not None:
                    # Set API key as environment variable
                    import os
                    old_api_key = os.environ.get('GROQ_API_KEY')
                    os.environ['GROQ_API_KEY'] = settings.GROQ_API_KEY
                    
                    try:
                        self.groq_client = Groq()
                        print("✅ GROQ API configured successfully")
                    except Exception as e:
                        print(f"❌ Error setting up GROQ API: {e}")
                        self.groq_client = None
                    finally:
                        # Restore environment variable
                        if old_api_key is not None:
                            os.environ['GROQ_API_KEY'] = old_api_key
                        elif 'GROQ_API_KEY' in os.environ:
                            del os.environ['GROQ_API_KEY']
                else:
                    print("❌ GROQ package is not available")
                    self.groq_client = None
            except Exception as e:
                print(f"❌ Error setting up GROQ API: {e}")
                self.groq_client = None
        else:
            self.groq_client = None
            print("⚠️ GROQ API not configured - using mock data")

    def get_google_trends_data(self, keywords: List[str], timeframe: str = "today 3-m") -> Dict[str, Any]:
        """
        الحصول على بيانات اتجاهات Google
        """
        if not self.pytrends:
            return {"success": False, "error": "Google Trends API not configured"}

        try:
            data = self._make_google_trends_request(keywords, timeframe)
            if not data["success"]:
                return data
            
            interest_over_time_df = data["interest_over_time_df"]
            interest_by_region_df = data["interest_by_region_df"]
            related_topics_dict = data["related_topics_dict"]
            related_queries_dict = data["related_queries_dict"]

            return {
                "success": True,
                "data": {
                    "interest_over_time": interest_over_time_df.astype(str).to_dict("index"),
                    "interest_by_region": interest_by_region_df.astype(str).to_dict("index"),
                    "related_topics": {k: v.astype(str).to_dict("records") for k, v in related_topics_dict.items()} if related_topics_dict else {},
                    "related_queries": {k: v.astype(str).to_dict("records") for k, v in related_queries_dict.items()} if related_queries_dict else {},
                    "keywords": keywords,
                    "timeframe": timeframe,
                    "source": "google_trends_api"
                }
            }

        except Exception as e:
            print(f"Error fetching Google Trends data: {e}")
            return {"success": False, "error": str(e)}

    def _make_google_trends_request(self, keywords: List[str], timeframe: str, retries: int = 10, delay: int = 60) -> Dict[str, Any]:
        """
        إجراء طلب Google Trends مع آلية إعادة المحاولة
        """
        for i in range(retries):
            try:
                self.pytrends.build_payload(
                    kw_list=keywords,
                    cat=0,
                    timeframe=timeframe
                )
                interest_over_time_df = self.pytrends.interest_over_time()
                interest_by_region_df = self.pytrends.interest_by_region(resolution='COUNTRY')
                related_topics_dict = self.pytrends.related_topics()
                related_queries_dict = self.pytrends.related_queries()
                return {
                    "success": True,
                    "interest_over_time_df": interest_over_time_df,
                    "interest_by_region_df": interest_by_region_df,
                    "related_topics_dict": related_topics_dict,
                    "related_queries_dict": related_queries_dict
                }
            except RequestException as e:
                if i < retries - 1:
                    print(f"Google Trends API rate limit hit or connection error. Retrying in {delay} seconds... ({e})")
                    time.sleep(delay)
                else:
                    return {"success": False, "error": f"Failed to fetch Google Trends data after {retries} retries: {e}"}
            except Exception as e:
                return {"success": False, "error": f"Error fetching Google Trends data: {e}"}
        return {"success": False, "error": "Unknown error during Google Trends request"}






    def generate_text_with_gemini(self, prompt: str, max_tokens: int = 200) -> Dict[str, Any]:
        """
        توليد نص باستخدام Google Gemini
        """
        if not self.gemini_model:
            return {
                "success": False,
                "error": "Gemini API not configured",
                "data": None
            }

        try:
            response = self.gemini_model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.7,
                    "max_output_tokens": max_tokens,
                    "candidate_count": 1
                }
            )

            return {
                "success": True,
                "data": {
                    "text": response.text.strip(),
                    "source": "gemini_api"
                }
            }

        except Exception as e:
            print(f"Error generating text with Gemini: {e}")
            return {
                "success": False,
                "error": str(e),
                "data": None
            }

    def get_available_groq_models(self) -> List[str]:
        """
        الحصول على قائمة بالنماذج المتاحة من GROQ API
        """
        if not self.groq_client:
            return []
        
        try:
            # Try to get available models from Groq API
            response = self.groq_client.models.list()
            all_models = [model.id for model in response.data]
            
            # Filter to only include text generation models
            text_models = []
            for model in all_models:
                # Exclude audio models (whisper), TTS models, and guard models
                if (not model.startswith('whisper') and 
                    not model.startswith('playai-tts') and 
                    'guard' not in model and 
                    'tts' not in model.lower()):
                    text_models.append(model)
            
            print(f"Found {len(all_models)} total models, {len(text_models)} text generation models")
            return text_models
        except Exception as e:
            print(f"Could not fetch available models from Groq: {e}")
            return []

    def generate_text_with_groq(self, prompt: str, max_tokens: int = 200) -> Dict[str, Any]:
        """
        توليد نص باستخدام GROQ
        """
        if not self.groq_client:
            return {
                "success": False,
                "error": "GROQ API not configured",
                "data": None
            }

        try:
            # Get available models dynamically
            available_models = self.get_available_groq_models()
            
            if available_models:
                # Use available models
                models_to_try = available_models
                print(f"Using available Groq models: {models_to_try}")
            else:
                # Fallback to hardcoded list with priority order
                models_to_try = [
                    "llama-3.1-8b-instant",
                    "llama-3.3-70b-versatile",
                    "meta-llama/llama-4-scout-17b-16e-instruct",
                    "deepseek-r1-distill-llama-70b",
                    "qwen/qwen3-32b",
                    "gemma2-9b-it",
                    "meta-llama/llama-4-maverick-17b-128e-instruct",
                    "allam-2-7b"
                ]
                print(f"Using fallback model list: {models_to_try}")
            
            last_error = None
            for model in models_to_try:
                try:
                    response = self.groq_client.chat.completions.create(
                        messages=[
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        model=model,
                        max_tokens=max_tokens,
                        temperature=0.7
                    )
                    return {
                        "success": True,
                        "data": {
                            "text": response.choices[0].message.content.strip(),
                            "source": "groq_api"
                        }
                    }
                except Exception as e:
                    last_error = e
                    print(f"Error with model {model}: {e}")
                    continue
            
            # If all models failed, return the last error
            print(f"Error generating text with GROQ: {last_error}")
            return {
                "success": False,
                "error": str(last_error),
                "data": None
            }

        except Exception as e:
            print(f"Error generating text with GROQ: {e}")
            return {
                "success": False,
                "error": str(e),
                "data": None
            }




    def validate_api_keys(self) -> Dict[str, bool]:
        """
        التحقق من صحة مفاتيح API
        """
        validation = {
            

            "groq_api": bool(settings.GROQ_API_KEY)
        
        }

        print("🔑 API Keys Validation:")


        print(f"  • GROQ API: {'✅ Configured' if validation['groq_api'] else '❌ Missing'}")

        return validation

    def get_api_status(self) -> Dict[str, Any]:
        """
        الحصول على حالة جميع الـ APIs
        """
        return {
            
            "google_trends_api": {
                "configured": bool(self.pytrends),
                "available": bool(self.pytrends)
            },

            "groq_api": {
                "configured": bool(self.groq_client),
                "available": bool(self.groq_client)
            }
        }


# إنشاء instance عام
api_integrations = APIIntegrations()