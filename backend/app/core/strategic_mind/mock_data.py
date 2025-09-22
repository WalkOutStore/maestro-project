"""
بيانات نموذجية لمحاكاة نتائج العقل الاستراتيجي
"""
import random
from typing import Dict, Any, List


def generate_ctr_prediction(campaign_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    توليد تنبؤ نموذجي لمعدل النقر إلى الظهور
    """
    # حساب التنبؤ بناءً على البيانات المدخلة
    base_ctr = 0.025
    
    # تعديل بناءً على الصناعة
    industry_factors = {
        'technology': 1.2,
        'retail': 1.0,
        'finance': 0.8,
        'healthcare': 0.9,
        'education': 1.1
    }
    
    # تعديل بناءً على القناة
    channel_factors = {
        'social_media': 1.1,
        'search_ads': 1.3,
        'display_ads': 0.7,
        'email': 0.9,
        'video': 1.4
    }
    
    # تعديل بناءً على نوع المحتوى
    content_factors = {
        'image': 1.0,
        'video': 1.3,
        'carousel': 1.1,
        'text': 0.8
    }
    
    industry = campaign_data.get('industry', 'technology')
    channel = campaign_data.get('channel', 'social_media')
    content_type = campaign_data.get('content_type', 'image')
    
    prediction = base_ctr * industry_factors.get(industry, 1.0) * \
                 channel_factors.get(channel, 1.0) * \
                 content_factors.get(content_type, 1.0)
    
    # إضافة عشوائية طفيفة
    prediction *= random.uniform(0.9, 1.1)
    
    return {
        "prediction": round(prediction, 4),
        "confidence": round(random.uniform(0.75, 0.95), 2),
        "explanation": [
            {
                "factor": "industry_factor",
                "importance": 0.3,
                "description": f"عامل الصناعة ({industry})"
            },
            {
                "factor": "channel_factor", 
                "importance": 0.4,
                "description": f"عامل القناة ({channel})"
            },
            {
                "factor": "content_factor",
                "importance": 0.2,
                "description": f"عامل المحتوى ({content_type})"
            },
            {
                "factor": "market_trends",
                "importance": 0.1,
                "description": "اتجاهات السوق الحالية"
            }
        ]
    }


def generate_roi_prediction(campaign_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    توليد تنبؤ نموذجي للعائد على الاستثمار
    """
    # حساب التنبؤ بناءً على البيانات المدخلة
    base_roi = 2.0
    
    # تعديل بناءً على الصناعة
    industry_factors = {
        'technology': 1.3,
        'retail': 1.1,
        'finance': 1.4,
        'healthcare': 1.2,
        'education': 0.9
    }
    
    # تعديل بناءً على القناة
    channel_factors = {
        'social_media': 1.0,
        'search_ads': 1.2,
        'display_ads': 0.8,
        'email': 1.4,
        'video': 1.1
    }
    
    # تعديل بناءً على الميزانية
    budget = campaign_data.get('budget', 5000)
    if budget > 10000:
        budget_factor = 1.2
    elif budget > 5000:
        budget_factor = 1.1
    else:
        budget_factor = 1.0
    
    industry = campaign_data.get('industry', 'technology')
    channel = campaign_data.get('channel', 'social_media')
    
    prediction = base_roi * industry_factors.get(industry, 1.0) * \
                 channel_factors.get(channel, 1.0) * budget_factor
    
    # إضافة عشوائية طفيفة
    prediction *= random.uniform(0.9, 1.1)
    
    return {
        "prediction": round(prediction, 2),
        "confidence": round(random.uniform(0.7, 0.9), 2),
        "explanation": [
            {
                "factor": "industry_performance",
                "importance": 0.35,
                "description": f"أداء الصناعة ({industry})"
            },
            {
                "factor": "channel_efficiency",
                "importance": 0.3,
                "description": f"كفاءة القناة ({channel})"
            },
            {
                "factor": "budget_optimization",
                "importance": 0.25,
                "description": f"تحسين الميزانية (${budget:,})"
            },
            {
                "factor": "market_conditions",
                "importance": 0.1,
                "description": "ظروف السوق الحالية"
            }
        ]
    }


def generate_channel_recommendations(campaign_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    توليد توصيات نموذجية للقنوات
    """
    industry = campaign_data.get('industry', 'technology')
    goal = campaign_data.get('goal', 'awareness')
    budget = campaign_data.get('budget', 5000)
    audience_age = campaign_data.get('audience_age', [25, 45])
    
    # قاعدة بيانات القنوات مع درجات الملاءمة
    channels_db = {
        'instagram': {
            'base_score': 0.8,
            'industry_bonus': {'retail': 0.1, 'technology': 0.05},
            'goal_bonus': {'awareness': 0.1, 'consideration': 0.05},
            'age_preference': [18, 35],
            'reason_template': 'منصة بصرية قوية مع جمهور نشط في الفئة العمرية المستهدفة'
        },
        'facebook': {
            'base_score': 0.75,
            'industry_bonus': {'retail': 0.08, 'finance': 0.1},
            'goal_bonus': {'awareness': 0.08, 'conversion': 0.1},
            'age_preference': [25, 55],
            'reason_template': 'تغطية واسعة مع خيارات استهداف متقدمة وأدوات تحليل قوية'
        },
        'google_ads': {
            'base_score': 0.85,
            'industry_bonus': {'technology': 0.1, 'finance': 0.08},
            'goal_bonus': {'conversion': 0.15, 'consideration': 0.1},
            'age_preference': [20, 60],
            'reason_template': 'فعال من حيث التكلفة مع إمكانية استهداف النوايا والكلمات المفتاحية'
        },
        'tiktok': {
            'base_score': 0.6,
            'industry_bonus': {'retail': 0.15, 'technology': 0.1},
            'goal_bonus': {'awareness': 0.2, 'consideration': 0.1},
            'age_preference': [16, 30],
            'reason_template': 'منصة متنامية بسرعة مع جمهور شاب نشط ومحتوى فيروسي'
        },
        'linkedin': {
            'base_score': 0.5,
            'industry_bonus': {'technology': 0.2, 'finance': 0.15, 'education': 0.1},
            'goal_bonus': {'consideration': 0.1, 'conversion': 0.05},
            'age_preference': [25, 50],
            'reason_template': 'شبكة مهنية مثالية للاستهداف B2B والمحتوى التعليمي'
        },
        'youtube': {
            'base_score': 0.7,
            'industry_bonus': {'technology': 0.1, 'education': 0.15},
            'goal_bonus': {'awareness': 0.1, 'consideration': 0.15},
            'age_preference': [18, 50],
            'reason_template': 'منصة فيديو رائدة مع إمكانيات استهداف متقدمة ومحتوى طويل المدى'
        }
    }
    
    recommendations = []
    
    for channel, data in channels_db.items():
        score = data['base_score']
        
        # إضافة مكافأة الصناعة
        if industry in data['industry_bonus']:
            score += data['industry_bonus'][industry]
        
        # إضافة مكافأة الهدف
        if goal in data['goal_bonus']:
            score += data['goal_bonus'][goal]
        
        # تعديل بناءً على الفئة العمرية
        age_min, age_max = audience_age
        pref_min, pref_max = data['age_preference']
        
        # حساب التداخل في الفئة العمرية
        overlap = max(0, min(age_max, pref_max) - max(age_min, pref_min))
        total_range = max(age_max, pref_max) - min(age_min, pref_min)
        age_factor = overlap / total_range if total_range > 0 else 0
        score += age_factor * 0.1
        
        # تعديل بناءً على الميزانية
        if budget > 10000:
            score += 0.05
        elif budget < 2000:
            score -= 0.1
        
        # إضافة عشوائية طفيفة
        score *= random.uniform(0.95, 1.05)
        
        # تحديد السبب
        reason = data['reason_template']
        if industry in data['industry_bonus']:
            reason += f" مع ملاءمة خاصة لصناعة {industry}"
        
        recommendations.append({
            'channel': channel,
            'score': min(1.0, max(0.0, score)),  # تحديد النطاق بين 0 و 1
            'reason': reason
        })
    
    # ترتيب التوصيات حسب الدرجة
    recommendations.sort(key=lambda x: x['score'], reverse=True)
    
    return recommendations[:5]  # إرجاع أفضل 5 قنوات
