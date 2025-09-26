from typing import Dict, Any, List, Optional, Tuple
import requests
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.models.knowledge_base import TrendData
from app.config import settings
from .api_integrations import api_integrations


class TrendAnalyzer:
    """
    محلل الاتجاهات للمساعدة في توليد محتوى إبداعي مناسب للاتجاهات الحالية
    """
    
    def __init__(self, db: Session = None):
        """
        تهيئة محلل الاتجاهات
        """
        self.db = db
        self.cache_duration = timedelta(days=1)  # مدة صلاحية البيانات المخزنة مؤقتًا
    
    def get_google_trends(self, keywords: List[str], timeframe: str = "today 3-m") -> Dict[str, Any]:
        """
        الحصول على بيانات اتجاهات Google للكلمات المفتاحية مع تحسينات للتحقق من صحة البيانات
        """
        # التحقق من صحة المدخلات
        if not self._validate_keywords(keywords):
            return self._get_error_response("Invalid keywords provided")

        # التحقق من صحة الإطار الزمني
        if not self._validate_timeframe(timeframe):
            return self._get_error_response("Invalid timeframe provided")

        # التحقق من وجود بيانات مخزنة مؤقتًا
        cached_data = self._get_cached_trends("google_trends", keywords, timeframe)
        if cached_data:
            return cached_data

        # استخدام خدمة التكامل مع الـ APIs
        trends_result = api_integrations.get_google_trends_data(keywords, timeframe)

        if trends_result["success"]:
            # التحقق من صحة البيانات المستلمة
            if self._validate_trend_data(trends_result["data"]):
                # تخزين البيانات مؤقتًا
                self._cache_trend_data("google_trends", keywords, timeframe, trends_result["data"])
                return trends_result["data"]
            else:
                return self._get_error_response("Invalid trend data received from API")
        else:
            # إذا فشل API، نعيد بيانات افتراضية
            return self._get_error_response(trends_result["error"])
    
    def get_twitter_trends(self, keywords: List[str], days: int = 7) -> Dict[str, Any]:
        """
        الحصول على بيانات اتجاهات Twitter للكلمات المفتاحية
        """
        # التحقق من وجود بيانات مخزنة مؤقتًا
        cached_data = self._get_cached_trends("twitter", keywords, f"days_{days}")
        if cached_data:
            return cached_data

        # استخدام خدمة التكامل مع الـ APIs
        twitter_result = api_integrations.get_twitter_data(keywords, days)

        if twitter_result["success"]:
            # تخزين البيانات مؤقتًا
            self._cache_trend_data("twitter", keywords, f"days_{days}", twitter_result["data"])
            return twitter_result["data"]
        else:
            # إذا فشل API، نعيد بيانات افتراضية
            return self._get_error_response(twitter_result["error"])
    
    def analyze_trends(self, campaign_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        تحليل الاتجاهات ذات الصلة بالحملة
        """
        # استخراج الكلمات المفتاحية من بيانات الحملة
        keywords = []
        if "product_description" in campaign_data:
            keywords.extend(campaign_data["product_description"].split())
        if "industry" in campaign_data:
            keywords.append(campaign_data["industry"])
        
        # تنظيف الكلمات المفتاحية
        keywords = [k.strip().lower() for k in keywords if len(k.strip()) > 3]
        keywords = list(set(keywords))[:5]  # أخذ أهم 5 كلمات مفتاحية
        
        # الحصول على بيانات الاتجاهات
        google_trends = self.get_google_trends(keywords)
        twitter_trends = self.get_twitter_trends(keywords)
        
        # تحليل البيانات
        analysis = self._analyze_trend_data(google_trends, twitter_trends, keywords)
        
        return {
            "keywords": keywords,
            "google_trends": google_trends,
            "twitter_trends": twitter_trends,
            "analysis": analysis
        }
    
    def _get_cached_trends(self, source: str, keywords: List[str], timeframe: str) -> Optional[Dict[str, Any]]:
        """
        الحصول على بيانات الاتجاهات المخزنة مؤقتًا
        """
        if self.db:
            # إنشاء مفتاح للبحث
            keyword_str = ",".join(sorted(keywords))
            
            # البحث عن البيانات المخزنة مؤقتًا
            trend_data = self.db.query(TrendData).filter(
                TrendData.keyword == keyword_str,
                TrendData.trend_source == f"{source}_{timeframe}",
                TrendData.timestamp > datetime.now() - self.cache_duration
            ).first()
            
            if trend_data:
                return trend_data.trend_data
        
        return None
    
    def _cache_trend_data(self, source: str, keywords: List[str], timeframe: str, data: Dict[str, Any]) -> None:
        """
        تخزين بيانات الاتجاهات مؤقتًا
        """
        if self.db:
            # إنشاء مفتاح للتخزين
            keyword_str = ",".join(sorted(keywords))
            
            # حساب قيمة الاتجاه (يمكن تنفيذ منطق أكثر تعقيدًا)
            trend_value = 0.5  # قيمة افتراضية
            
            # إنشاء كائن TrendData جديد
            trend_data = TrendData(
                keyword=keyword_str,
                trend_source=f"{source}_{timeframe}",
                trend_value=trend_value,
                trend_data=data
            )
            
            self.db.add(trend_data)
            self.db.commit()
    
    def _generate_mock_google_trends(self, keywords: List[str], timeframe: str) -> Dict[str, Any]:
        """
        توليد بيانات اتجاهات Google مزيفة للاختبار
        """
        # إنشاء تواريخ للبيانات
        if timeframe == "today 3-m":
            dates = pd.date_range(end=datetime.now(), periods=90, freq="D")
        elif timeframe == "today 1-m":
            dates = pd.date_range(end=datetime.now(), periods=30, freq="D")
        else:
            dates = pd.date_range(end=datetime.now(), periods=7, freq="D")
        
        # إنشاء بيانات مزيفة لكل كلمة مفتاحية
        interest_over_time = {}
        for keyword in keywords:
            # توليد قيم عشوائية مع اتجاه تصاعدي
            base = np.random.randint(30, 70)
            trend = np.random.choice([0.1, 0.2, -0.1])  # اتجاه تصاعدي أو تنازلي
            noise = np.random.normal(0, 5, len(dates))
            values = [max(0, min(100, base + i * trend + noise[i])) for i in range(len(dates))]
            
            interest_over_time[keyword] = values
        
        # إضافة التواريخ
        interest_over_time["dates"] = [d.strftime("%Y-%m-%d") for d in dates]
        
        # إنشاء بيانات المناطق
        regions = ["United States", "United Kingdom", "Canada", "Australia", "Germany"]
        interest_by_region = {}
        for keyword in keywords:
            interest_by_region[keyword] = {region: np.random.randint(0, 100) for region in regions}
        
        # إنشاء مواضيع ذات صلة
        related_topics = {}
        for keyword in keywords:
            related_topics[keyword] = [
                {"title": f"Topic related to {keyword} 1", "value": np.random.randint(50, 100)},
                {"title": f"Topic related to {keyword} 2", "value": np.random.randint(30, 80)},
                {"title": f"Topic related to {keyword} 3", "value": np.random.randint(20, 60)}
            ]
        
        # إنشاء استعلامات ذات صلة
        related_queries = {}
        for keyword in keywords:
            related_queries[keyword] = [
                {"query": f"{keyword} best", "value": np.random.randint(50, 100)},
                {"query": f"{keyword} how to", "value": np.random.randint(30, 80)},
                {"query": f"{keyword} vs", "value": np.random.randint(20, 60)}
            ]
        
        return {
            "interest_over_time": interest_over_time,
            "interest_by_region": interest_by_region,
            "related_topics": related_topics,
            "related_queries": related_queries
        }
    
    def _generate_mock_twitter_trends(self, keywords: List[str], days: int) -> Dict[str, Any]:
        """
        توليد بيانات اتجاهات Twitter مزيفة للاختبار
        """
        # إنشاء تواريخ للبيانات
        dates = pd.date_range(end=datetime.now(), periods=days, freq="D")
        
        # إنشاء بيانات مزيفة لكل كلمة مفتاحية
        tweets_volume = {}
        sentiment = {}
        
        for keyword in keywords:
            # توليد حجم التغريدات
            base_volume = np.random.randint(100, 1000)
            noise = np.random.normal(0, base_volume * 0.2, days)
            volumes = [max(0, int(base_volume + noise[i])) for i in range(days)]
            tweets_volume[keyword] = {dates[i].strftime("%Y-%m-%d"): volumes[i] for i in range(days)}
            
            # توليد بيانات المشاعر
            sentiment[keyword] = {
                "positive": np.random.uniform(0.3, 0.6),
                "neutral": np.random.uniform(0.2, 0.4),
                "negative": np.random.uniform(0.1, 0.3)
            }
            # تطبيع القيم
            total = sum(sentiment[keyword].values())
            sentiment[keyword] = {k: v / total for k, v in sentiment[keyword].items()}
        
        # إنشاء هاشتاجات شائعة
        hashtags = {}
        for keyword in keywords:
            hashtags[keyword] = [
                {"tag": f"#{keyword.replace(' ', '')}", "count": np.random.randint(50, 500)},
                {"tag": f"#{keyword.replace(' ', '')}Challenge", "count": np.random.randint(30, 300)},
                {"tag": f"#{keyword.replace(' ', '')}Tips", "count": np.random.randint(20, 200)}
            ]
        
        return {
            "volume": tweets_volume,
            "sentiment": sentiment,
            "hashtags": hashtags,
            "dates": [d.strftime("%Y-%m-%d") for d in dates]
        }
    
    def _analyze_trend_data(self, google_trends: Dict[str, Any], twitter_trends: Dict[str, Any], keywords: List[str]) -> Dict[str, Any]:
        """
        تحليل بيانات الاتجاهات وتقديم توصيات
        """
        analysis = {
            "trending_keywords": [],
            "sentiment": {},
            "recommendations": []
        }
        
        # تحليل الكلمات المفتاحية الرائجة
        for keyword in keywords:
            # حساب متوسط الاهتمام في Google Trends
            if "interest_over_time" in google_trends and keyword in google_trends["interest_over_time"]:
                avg_interest = sum(google_trends["interest_over_time"][keyword]) / len(google_trends["interest_over_time"][keyword])
            else:
                avg_interest = 50  # قيمة افتراضية
            
            # حساب متوسط حجم التغريدات
            if "volume" in twitter_trends and keyword in twitter_trends["volume"]:
                avg_volume = sum(twitter_trends["volume"][keyword].values()) / len(twitter_trends["volume"][keyword])
            else:
                avg_volume = 100  # قيمة افتراضية
            
            # حساب درجة الاتجاه
            trend_score = (avg_interest / 100 * 0.6) + (min(avg_volume, 1000) / 1000 * 0.4)
            
            analysis["trending_keywords"].append({
                "keyword": keyword,
                "trend_score": trend_score,
                "google_interest": avg_interest,
                "twitter_volume": avg_volume
            })
        
        # ترتيب الكلمات المفتاحية حسب درجة الاتجاه
        analysis["trending_keywords"].sort(key=lambda x: x["trend_score"], reverse=True)
        
        # تحليل المشاعر
        for keyword in keywords:
            if "sentiment" in twitter_trends and keyword in twitter_trends["sentiment"]:
                analysis["sentiment"][keyword] = twitter_trends["sentiment"][keyword]
            else:
                # قيم افتراضية
                analysis["sentiment"][keyword] = {
                    "positive": 0.4,
                    "neutral": 0.4,
                    "negative": 0.2
                }
        
        # توصيات بناءً على التحليل
        # الكلمة المفتاحية الأكثر رواجًا
        if analysis["trending_keywords"]:
            top_keyword = analysis["trending_keywords"][0]["keyword"]
            analysis["recommendations"].append({
                "type": "keyword_focus",
                "description": f"Focus on '{top_keyword}' in your campaign as it shows the highest trend score.",
                "score": analysis["trending_keywords"][0]["trend_score"]
            })
        
        # توصيات بناءً على المشاعر
        for keyword, sentiment_data in analysis["sentiment"].items():
            if sentiment_data["positive"] > 0.5:
                analysis["recommendations"].append({
                    "type": "positive_sentiment",
                    "description": f"Leverage the positive sentiment around '{keyword}' in your messaging.",
                    "score": sentiment_data["positive"]
                })
            elif sentiment_data["negative"] > 0.3:
                analysis["recommendations"].append({
                    "type": "address_concerns",
                    "description": f"Address potential concerns around '{keyword}' in your campaign.",
                    "score": sentiment_data["negative"]
                })
        
        # توصيات بناءً على الهاشتاجات الشائعة
        if "hashtags" in twitter_trends:
            for keyword in keywords:
                if keyword in twitter_trends["hashtags"] and twitter_trends["hashtags"][keyword]:
                    top_hashtag = twitter_trends["hashtags"][keyword][0]["tag"]
                    analysis["recommendations"].append({
                        "type": "hashtag_use",
                        "description": f"Include the popular hashtag {top_hashtag} in your social media posts.",
                        "score": twitter_trends["hashtags"][keyword][0]["count"] / 500  # تطبيع الدرجة
                    })
        
        # ترتيب التوصيات حسب الدرجة
        analysis["recommendations"].sort(key=lambda x: x["score"], reverse=True)
        
        return analysis
    
    def _validate_keywords(self, keywords: List[str]) -> bool:
        """
        التحقق من صحة الكلمات المفتاحية
        """
        if not keywords or len(keywords) < 1:
            return False
        for keyword in keywords:
            if not isinstance(keyword, str) or len(keyword.strip()) < 3:
                return False
        return True
    
    def _validate_timeframe(self, timeframe: str) -> bool:
        """
        التحقق من صحة الإطار الزمني
        """
        valid_timeframes = ["today 3-m", "today 1-m", "today 7-d"]
        return timeframe in valid_timeframes
    
    def _validate_trend_data(self, trend_data: Dict[str, Any]) -> bool:
        """
        التحقق من صحة بيانات الاتجاهات
        """
        if not trend_data or not isinstance(trend_data, dict):
            return False
        required_keys = ["interest_over_time", "interest_by_region", "related_topics", "related_queries"]
        for key in required_keys:
            if key not in trend_data:
                return False
        return True
    
    def _get_error_response(self, error_message: str) -> Dict[str, Any]:
        """
        إرجاع استجابة خطأ
        """
        return {
            "success": False,
            "error": error_message
        }