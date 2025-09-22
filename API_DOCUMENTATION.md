# توثيق واجهات برمجة التطبيقات (API) لمنصة Maestro

هذا المستند يوفر توثيقًا شاملاً لواجهات برمجة التطبيقات (APIs) المتاحة في منصة Maestro للتسويق الرقمي المدعومة بالذكاء الاصطناعي.

## معلومات عامة

- **عنوان القاعدة**: `http://localhost:8000/api/v1`
- **تنسيق البيانات**: JSON
- **المصادقة**: Bearer Token (JWT)
- **توثيق Swagger**: متاح على `http://localhost:8000/docs`
- **توثيق ReDoc**: متاح على `http://localhost:8000/redoc`

## المصادقة

جميع نقاط النهاية (endpoints) تتطلب مصادقة باستثناء تسجيل الدخول وإنشاء مستخدم جديد.

### الحصول على رمز الوصول (Access Token)

```
POST /api/v1/users/login
```

**طلب**:

```json
{
  "username": "user@example.com",
  "password": "password123"
}
```

**استجابة**:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### استخدام رمز الوصول

أضف رأس `Authorization` إلى جميع الطلبات:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## واجهات برمجة التطبيقات (APIs)

### المستخدمين

#### إنشاء مستخدم جديد

```
POST /api/v1/users
```

**طلب**:

```json
{
  "email": "user@example.com",
  "username": "username",
  "full_name": "الاسم الكامل",
  "password": "password123",
  "is_active": true
}
```

**استجابة**:

```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "full_name": "الاسم الكامل",
  "is_active": true,
  "created_at": "2023-06-01T12:00:00"
}
```

#### الحصول على بيانات المستخدم الحالي

```
GET /api/v1/users/me
```

**استجابة**:

```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "full_name": "الاسم الكامل",
  "is_active": true,
  "created_at": "2023-06-01T12:00:00"
}
```

#### تحديث بيانات المستخدم الحالي

```
PUT /api/v1/users/me
```

**طلب**:

```json
{
  "full_name": "الاسم الكامل المحدث",
  "password": "new_password123"
}
```

**استجابة**:

```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "full_name": "الاسم الكامل المحدث",
  "is_active": true,
  "created_at": "2023-06-01T12:00:00"
}
```

### الحملات

#### الحصول على قائمة الحملات

```
GET /api/v1/campaigns
```

**معلمات الاستعلام**:

- `skip` (اختياري): عدد العناصر التي يتم تخطيها (للصفحات)
- `limit` (اختياري): الحد الأقصى لعدد العناصر المُرجعة
- `status` (اختياري): تصفية حسب الحالة (active, planned, completed)

**استجابة**:

```json
{
  "total": 10,
  "items": [
    {
      "id": 1,
      "name": "حملة إطلاق المنتج الجديد",
      "description": "حملة تسويقية لإطلاق المنتج الجديد",
      "status": "active",
      "budget": 5000,
      "start_date": "2023-06-01",
      "end_date": "2023-07-01",
      "created_at": "2023-05-15T10:30:00",
      "updated_at": "2023-05-15T10:30:00",
      "user_id": 1,
      "metrics": {
        "impressions": 120000,
        "clicks": 3600,
        "ctr": 0.03,
        "conversions": 180,
        "roi": 2.5
      }
    },
    // المزيد من الحملات...
  ]
}
```

#### إنشاء حملة جديدة

```
POST /api/v1/campaigns
```

**طلب**:

```json
{
  "name": "حملة تسويقية جديدة",
  "description": "وصف الحملة التسويقية",
  "status": "planned",
  "budget": 3000,
  "start_date": "2023-07-01",
  "end_date": "2023-08-01",
  "target_audience": {
    "age_range": [25, 45],
    "gender": "all",
    "interests": ["technology", "marketing"],
    "locations": ["Saudi Arabia", "UAE"]
  },
  "channels": ["social_media", "email", "search_ads"]
}
```

**استجابة**:

```json
{
  "id": 3,
  "name": "حملة تسويقية جديدة",
  "description": "وصف الحملة التسويقية",
  "status": "planned",
  "budget": 3000,
  "start_date": "2023-07-01",
  "end_date": "2023-08-01",
  "created_at": "2023-06-15T14:20:00",
  "updated_at": "2023-06-15T14:20:00",
  "user_id": 1,
  "target_audience": {
    "age_range": [25, 45],
    "gender": "all",
    "interests": ["technology", "marketing"],
    "locations": ["Saudi Arabia", "UAE"]
  },
  "channels": ["social_media", "email", "search_ads"],
  "metrics": {
    "impressions": 0,
    "clicks": 0,
    "ctr": 0,
    "conversions": 0,
    "roi": 0
  }
}
```

#### الحصول على تفاصيل حملة

```
GET /api/v1/campaigns/{campaign_id}
```

**استجابة**:

```json
{
  "id": 1,
  "name": "حملة إطلاق المنتج الجديد",
  "description": "حملة تسويقية لإطلاق المنتج الجديد",
  "status": "active",
  "budget": 5000,
  "start_date": "2023-06-01",
  "end_date": "2023-07-01",
  "created_at": "2023-05-15T10:30:00",
  "updated_at": "2023-05-15T10:30:00",
  "user_id": 1,
  "target_audience": {
    "age_range": [25, 45],
    "gender": "all",
    "interests": ["technology", "innovation"],
    "locations": ["Saudi Arabia", "UAE", "Kuwait"]
  },
  "channels": ["social_media", "search_ads", "display_ads"],
  "metrics": {
    "impressions": 120000,
    "clicks": 3600,
    "ctr": 0.03,
    "conversions": 180,
    "roi": 2.5
  },
  "contents": [
    {
      "id": 1,
      "type": "ad_copy",
      "title": "اكتشف الابتكار الجديد",
      "content": "منتجنا الجديد يغير قواعد اللعبة. اكتشفه الآن!",
      "channel": "social_media",
      "status": "active",
      "performance": {
        "impressions": 45000,
        "clicks": 1500,
        "ctr": 0.033
      }
    },
    // المزيد من المحتوى...
  ],
  "recommendations": [
    {
      "id": 1,
      "type": "budget_allocation",
      "content": "زيادة ميزانية إعلانات البحث بنسبة 20%",
      "confidence": 0.85,
      "status": "pending",
      "created_at": "2023-06-10T09:15:00"
    },
    // المزيد من التوصيات...
  ]
}
```

#### تحديث حملة

```
PUT /api/v1/campaigns/{campaign_id}
```

**طلب**:

```json
{
  "name": "حملة إطلاق المنتج الجديد - محدثة",
  "budget": 6000,
  "status": "active"
}
```

**استجابة**:

```json
{
  "id": 1,
  "name": "حملة إطلاق المنتج الجديد - محدثة",
  "description": "حملة تسويقية لإطلاق المنتج الجديد",
  "status": "active",
  "budget": 6000,
  "start_date": "2023-06-01",
  "end_date": "2023-07-01",
  "created_at": "2023-05-15T10:30:00",
  "updated_at": "2023-06-15T16:45:00",
  "user_id": 1,
  // باقي البيانات...
}
```

#### حذف حملة

```
DELETE /api/v1/campaigns/{campaign_id}
```

**استجابة**:

```json
{
  "message": "تم حذف الحملة بنجاح"
}
```

### العقل الاستراتيجي (Strategic Mind)

#### التنبؤ بمعدل النقر إلى الظهور (CTR)

```
POST /api/v1/strategic-mind/predict-ctr
```

**طلب**:

```json
{
  "industry": "technology",
  "channel": "social_media",
  "audience_age": [25, 45],
  "budget": 5000,
  "content_type": "video",
  "campaign_id": 1
}
```

**استجابة**:

```json
{
  "prediction": 0.032,
  "confidence": 0.85,
  "factors": [
    {"name": "جودة المحتوى", "value": 0.35},
    {"name": "دقة الاستهداف", "value": 0.25},
    {"name": "متوسط الصناعة", "value": 0.20},
    {"name": "الاتجاهات الموسمية", "value": 0.15},
    {"name": "عوامل أخرى", "value": 0.05}
  ],
  "benchmark": 0.025,
  "prediction_id": "pred_ctr_123456"
}
```

#### التنبؤ بالعائد على الاستثمار (ROI)

```
POST /api/v1/strategic-mind/predict-roi
```

**طلب**:

```json
{
  "industry": "technology",
  "channel": "social_media",
  "budget": 5000,
  "duration": 30,
  "campaign_id": 1
}
```

**استجابة**:

```json
{
  "prediction": 2.4,
  "confidence": 0.8,
  "trend": [
    {"name": "يناير", "value": 1.8},
    {"name": "فبراير", "value": 2.0},
    {"name": "مارس", "value": 2.2},
    {"name": "أبريل", "value": 2.1},
    {"name": "مايو", "value": 2.4},
    {"name": "يونيو", "value": 2.6}
  ],
  "benchmark": 2.1,
  "prediction_id": "pred_roi_123456"
}
```

#### توصية بقنوات التسويق

```
POST /api/v1/strategic-mind/recommend-channels
```

**طلب**:

```json
{
  "industry": "technology",
  "audience_age": [25, 45],
  "budget": 5000,
  "goal": "awareness",
  "campaign_id": 1
}
```

**استجابة**:

```json
{
  "recommendations": [
    {
      "channel": "instagram",
      "score": 0.85,
      "reason": "مناسب للفئة العمرية المستهدفة مع تركيز على الوعي بالعلامة التجارية"
    },
    {
      "channel": "facebook",
      "score": 0.75,
      "reason": "تغطية واسعة مع خيارات استهداف متقدمة"
    },
    {
      "channel": "google_ads",
      "score": 0.70,
      "reason": "فعال من حيث التكلفة مع إمكانية استهداف النوايا"
    },
    {
      "channel": "tiktok",
      "score": 0.65,
      "reason": "منصة متنامية مع جمهور شاب نشط"
    },
    {
      "channel": "linkedin",
      "score": 0.45,
      "reason": "أقل ملاءمة للأهداف الحالية والفئة العمرية"
    }
  ],
  "recommendation_id": "rec_channels_123456"
}
```

### الشرارة الإبداعية (Creative Spark)

#### توليد نص إعلاني

```
POST /api/v1/creative-spark/generate-ad-copy
```

**طلب**:

```json
{
  "campaign_id": 1,
  "product_name": "تطبيق إدارة المهام",
  "key_features": ["سهل الاستخدام", "مزامنة سحابية", "تذكيرات ذكية"],
  "target_audience": "المهنيين المشغولين",
  "tone": "professional",
  "content_type": "social_post",
  "max_length": 150
}
```

**استجابة**:

```json
{
  "ad_copies": [
    {
      "title": "أنجز أكثر، اعمل أقل",
      "content": "تطبيق إدارة المهام الجديد يساعدك على تنظيم يومك بذكاء. مزامنة سحابية، تذكيرات ذكية، وواجهة سهلة الاستخدام. جرّبه الآن!",
      "cta": "تحميل التطبيق",
      "score": 0.92
    },
    {
      "title": "وقتك ثمين، استثمره بذكاء",
      "content": "للمهنيين المشغولين: تطبيق إدارة المهام الذي يفهم أولوياتك. سهل الاستخدام مع مزامنة سحابية لجميع أجهزتك.",
      "cta": "ابدأ مجانًا",
      "score": 0.88
    },
    {
      "title": "التنظيم الذكي لمهامك اليومية",
      "content": "تذكيرات ذكية، مزامنة فورية، وواجهة بسيطة. كل ما تحتاجه لإدارة مهامك في مكان واحد.",
      "cta": "اكتشف الآن",
      "score": 0.85
    }
  ],
  "generation_id": "gen_adcopy_123456"
}
```

#### توليد اقتراحات بصرية

```
POST /api/v1/creative-spark/generate-visual-suggestions
```

**طلب**:

```json
{
  "campaign_id": 1,
  "product_type": "software",
  "brand_colors": ["#3498db", "#2ecc71", "#ecf0f1"],
  "style": "modern",
  "content_type": "social_media_post",
  "key_message": "سهولة الاستخدام والإنتاجية"
}
```

**استجابة**:

```json
{
  "visual_suggestions": [
    {
      "description": "صورة لشخص يستخدم التطبيق على هاتفه بسهولة، مع رسوم بيانية بسيطة تظهر زيادة الإنتاجية",
      "elements": ["شخص", "هاتف ذكي", "رسم بياني", "واجهة التطبيق"],
      "colors": ["#3498db", "#2ecc71", "#ecf0f1"],
      "composition": "close-up",
      "mood": "productive",
      "score": 0.94
    },
    {
      "description": "مقارنة بين قائمة مهام فوضوية على الورق وقائمة منظمة في التطبيق، مع تسليط الضوء على الفرق",
      "elements": ["قائمة مهام ورقية", "شاشة التطبيق", "تباين", "تنظيم"],
      "colors": ["#3498db", "#ecf0f1", "#e74c3c"],
      "composition": "split-screen",
      "mood": "transformative",
      "score": 0.89
    },
    {
      "description": "صورة لسطح مكتب منظم مع جهاز لوحي يعرض التطبيق، وساعة تشير إلى توفير الوقت",
      "elements": ["سطح مكتب", "جهاز لوحي", "ساعة", "أدوات مكتبية منظمة"],
      "colors": ["#2ecc71", "#ecf0f1", "#3498db"],
      "composition": "flat-lay",
      "mood": "organized",
      "score": 0.87
    }
  ],
  "generation_id": "gen_visual_123456"
}
```

#### تحليل اتجاهات المحتوى

```
POST /api/v1/creative-spark/analyze-trends
```

**طلب**:

```json
{
  "industry": "technology",
  "content_type": "social_media",
  "time_period": "last_3_months",
  "target_audience": {
    "age_range": [25, 45],
    "interests": ["productivity", "technology", "business"]
  }
}
```

**استجابة**:

```json
{
  "trends": [
    {
      "name": "محتوى الفيديو القصير",
      "popularity": 0.92,
      "growth_rate": 0.15,
      "platforms": ["TikTok", "Instagram Reels", "YouTube Shorts"],
      "description": "مقاطع فيديو قصيرة (15-60 ثانية) تعرض ميزات المنتج بطريقة سريعة وجذابة"
    },
    {
      "name": "محتوى تعليمي",
      "popularity": 0.85,
      "growth_rate": 0.08,
      "platforms": ["LinkedIn", "YouTube", "Instagram"],
      "description": "محتوى يشرح كيفية استخدام المنتج لحل مشكلات محددة أو تحسين الإنتاجية"
    },
    {
      "name": "قصص المستخدمين",
      "popularity": 0.78,
      "growth_rate": 0.12,
      "platforms": ["Instagram", "LinkedIn", "Facebook"],
      "description": "قصص حقيقية من مستخدمين يشاركون تجاربهم مع المنتج وكيف ساعدهم"
    },
    {
      "name": "تحديات تفاعلية",
      "popularity": 0.72,
      "growth_rate": 0.18,
      "platforms": ["TikTok", "Instagram", "Twitter"],
      "description": "تحديات تشجع المستخدمين على مشاركة إنجازاتهم باستخدام المنتج"
    }
  ],
  "keywords": [
    {"word": "إنتاجية", "volume": 0.85},
    {"word": "توفير الوقت", "volume": 0.82},
    {"word": "عمل عن بعد", "volume": 0.78},
    {"word": "تنظيم", "volume": 0.75},
    {"word": "تعاون", "volume": 0.70}
  ],
  "analysis_id": "trend_analysis_123456"
}
```

### المرشد الشفاف (Transparent Mentor)

#### شرح التنبؤات

```
POST /api/v1/transparent-mentor/explain-prediction
```

**طلب**:

```json
{
  "prediction_id": "pred_ctr_123456",
  "model_type": "ctr",
  "detail_level": "detailed"
}
```

**استجابة**:

```json
{
  "explanation": {
    "summary": "تم التنبؤ بمعدل نقر إلى ظهور بنسبة 3.2% بناءً على تحليل عوامل متعددة، وهو أعلى من متوسط الصناعة البالغ 2.5%.",
    "factors": [
      {
        "name": "جودة المحتوى",
        "importance": 0.35,
        "description": "محتوى الفيديو يميل إلى تحقيق معدلات نقر أعلى بنسبة 30% من الصور الثابتة في هذه الصناعة."
      },
      {
        "name": "دقة الاستهداف",
        "importance": 0.25,
        "description": "الفئة العمرية المستهدفة (25-45) تتفاعل بشكل جيد مع إعلانات التكنولوجيا على وسائل التواصل الاجتماعي."
      },
      {
        "name": "متوسط الصناعة",
        "importance": 0.20,
        "description": "متوسط معدل النقر إلى الظهور في صناعة التكنولوجيا هو 2.5%."
      },
      {
        "name": "الاتجاهات الموسمية",
        "importance": 0.15,
        "description": "الربع الثاني من العام يشهد عادةً زيادة في معدلات النقر بنسبة 10-15%."
      },
      {
        "name": "عوامل أخرى",
        "importance": 0.05,
        "description": "عوامل متنوعة مثل سرعة تحميل الصفحة وتصميم الإعلان."
      }
    ],
    "model_information": {
      "type": "Hybrid (Rule-based + Gradient Boosting)",
      "features_used": 24,
      "training_data_period": "2022-01 to 2023-05",
      "accuracy": 0.85
    },
    "visualization_configs": {
      "factor_importance": {
        "type": "bar_chart",
        "data": [
          {"name": "جودة المحتوى", "value": 0.35},
          {"name": "دقة الاستهداف", "value": 0.25},
          {"name": "متوسط الصناعة", "value": 0.20},
          {"name": "الاتجاهات الموسمية", "value": 0.15},
          {"name": "عوامل أخرى", "value": 0.05}
        ]
      },
      "industry_comparison": {
        "type": "gauge_chart",
        "value": 0.032,
        "min": 0,
        "max": 0.06,
        "ranges": [
          {"min": 0, "max": 0.02, "label": "منخفض", "color": "#e74c3c"},
          {"min": 0.02, "max": 0.04, "label": "متوسط", "color": "#f39c12"},
          {"min": 0.04, "max": 0.06, "label": "مرتفع", "color": "#2ecc71"}
        ],
        "benchmark": 0.025
      }
    }
  },
  "explanation_id": "exp_pred_123456"
}
```

#### شرح التوصيات

```
POST /api/v1/transparent-mentor/explain-recommendation
```

**طلب**:

```json
{
  "recommendation_id": "rec_channels_123456",
  "recommendation_type": "channel",
  "detail_level": "detailed"
}
```

**استجابة**:

```json
{
  "explanation": {
    "summary": "تم التوصية بـ Instagram كأفضل قناة تسويقية لحملتك بناءً على تحليل الجمهور المستهدف وهدف الحملة والميزانية.",
    "recommendations": [
      {
        "channel": "instagram",
        "score": 0.85,
        "reason": "مناسب للفئة العمرية المستهدفة (25-45) مع تركيز على الوعي بالعلامة التجارية",
        "detailed_reasons": [
          "85% من جمهورك المستهدف نشط على Instagram",
          "المحتوى البصري فعال لزيادة الوعي بالعلامة التجارية",
          "تكلفة النقرة أقل بنسبة 20% من المتوسط لهذه الفئة العمرية",
          "معدلات المشاركة أعلى بنسبة 30% من المنصات الأخرى"
        ]
      },
      {
        "channel": "facebook",
        "score": 0.75,
        "reason": "تغطية واسعة مع خيارات استهداف متقدمة",
        "detailed_reasons": [
          "تغطية واسعة للفئة العمرية المستهدفة",
          "خيارات استهداف متقدمة تناسب أهداف الحملة",
          "فعال من حيث التكلفة للميزانية المحددة",
          "أداء جيد في حملات الوعي بالعلامة التجارية"
        ]
      },
      // المزيد من القنوات...
    ],
    "decision_factors": [
      {
        "name": "ملاءمة الجمهور المستهدف",
        "weight": 0.40,
        "description": "مدى تطابق الفئة العمرية والاهتمامات مع مستخدمي القناة"
      },
      {
        "name": "فعالية التكلفة",
        "weight": 0.25,
        "description": "العائد المتوقع مقابل الإنفاق على القناة"
      },
      {
        "name": "ملاءمة هدف الحملة",
        "weight": 0.20,
        "description": "مدى فعالية القناة في تحقيق هدف الوعي بالعلامة التجارية"
      },
      {
        "name": "أداء سابق",
        "weight": 0.15,
        "description": "أداء القناة في حملات مشابهة سابقة"
      }
    ],
    "visualization_configs": {
      "channel_scores": {
        "type": "horizontal_bar_chart",
        "data": [
          {"name": "Instagram", "value": 0.85},
          {"name": "Facebook", "value": 0.75},
          {"name": "Google Ads", "value": 0.70},
          {"name": "TikTok", "value": 0.65},
          {"name": "LinkedIn", "value": 0.45}
        ]
      },
      "decision_tree": {
        "type": "tree_diagram",
        "root": "اختيار القناة",
        "branches": [
          {
            "name": "ملاءمة الجمهور",
            "children": [
              {"name": "Instagram", "value": "عالي"},
              {"name": "Facebook", "value": "متوسط-عالي"},
              {"name": "TikTok", "value": "متوسط"}
            ]
          },
          {
            "name": "فعالية التكلفة",
            "children": [
              {"name": "Google Ads", "value": "عالي"},
              {"name": "Instagram", "value": "متوسط-عالي"},
              {"name": "Facebook", "value": "متوسط"}
            ]
          }
        ]
      }
    }
  },
  "explanation_id": "exp_rec_123456"
}
```

#### توليد سيناريوهات بديلة

```
POST /api/v1/transparent-mentor/generate-alternative-scenarios
```

**طلب**:

```json
{
  "campaign_id": 1,
  "base_scenario": {
    "budget": 5000,
    "channels": ["instagram", "facebook", "google_ads"],
    "budget_allocation": {"instagram": 0.5, "facebook": 0.3, "google_ads": 0.2}
  },
  "scenario_type": "budget_allocation",
  "num_scenarios": 3
}
```

**استجابة**:

```json
{
  "scenarios": [
    {
      "name": "السيناريو الأساسي",
      "description": "التوزيع الحالي للميزانية",
      "budget_allocation": {"instagram": 0.5, "facebook": 0.3, "google_ads": 0.2},
      "predicted_metrics": {
        "impressions": 120000,
        "clicks": 3600,
        "ctr": 0.03,
        "conversions": 180,
        "roi": 2.5
      }
    },
    {
      "name": "سيناريو التركيز على Instagram",
      "description": "زيادة ميزانية Instagram مع تقليل Facebook",
      "budget_allocation": {"instagram": 0.65, "facebook": 0.15, "google_ads": 0.2},
      "predicted_metrics": {
        "impressions": 135000,
        "clicks": 4050,
        "ctr": 0.03,
        "conversions": 202,
        "roi": 2.7
      },
      "comparison": {
        "impressions": "+12.5%",
        "clicks": "+12.5%",
        "conversions": "+12.2%",
        "roi": "+8.0%"
      }
    },
    {
      "name": "سيناريو متوازن",
      "description": "توزيع متساوٍ بين القنوات الثلاث",
      "budget_allocation": {"instagram": 0.33, "facebook": 0.33, "google_ads": 0.34},
      "predicted_metrics": {
        "impressions": 110000,
        "clicks": 3300,
        "ctr": 0.03,
        "conversions": 165,
        "roi": 2.3
      },
      "comparison": {
        "impressions": "-8.3%",
        "clicks": "-8.3%",
        "conversions": "-8.3%",
        "roi": "-8.0%"
      }
    },
    {
      "name": "سيناريو التركيز على Google Ads",
      "description": "زيادة ميزانية Google Ads مع تقليل Facebook",
      "budget_allocation": {"instagram": 0.5, "facebook": 0.1, "google_ads": 0.4},
      "predicted_metrics": {
        "impressions": 105000,
        "clicks": 3675,
        "ctr": 0.035,
        "conversions": 184,
        "roi": 2.6
      },
      "comparison": {
        "impressions": "-12.5%",
        "clicks": "+2.1%",
        "conversions": "+2.2%",
        "roi": "+4.0%"
      }
    }
  ],
  "visualization_configs": {
    "roi_comparison": {
      "type": "bar_chart",
      "data": [
        {"name": "السيناريو الأساسي", "value": 2.5},
        {"name": "التركيز على Instagram", "value": 2.7},
        {"name": "متوازن", "value": 2.3},
        {"name": "التركيز على Google Ads", "value": 2.6}
      ]
    },
    "budget_allocation": {
      "type": "stacked_bar_chart",
      "data": [
        {
          "name": "السيناريو الأساسي",
          "instagram": 2500,
          "facebook": 1500,
          "google_ads": 1000
        },
        {
          "name": "التركيز على Instagram",
          "instagram": 3250,
          "facebook": 750,
          "google_ads": 1000
        },
        {
          "name": "متوازن",
          "instagram": 1650,
          "facebook": 1650,
          "google_ads": 1700
        },
        {
          "name": "التركيز على Google Ads",
          "instagram": 2500,
          "facebook": 500,
          "google_ads": 2000
        }
      ]
    }
  },
  "generation_id": "gen_scenarios_123456"
}
```

### حلقة التعلم التشاركي (Learning Loop)

#### حفظ التغذية الراجعة على التوصيات

```
POST /api/v1/learning-loop/save-recommendation-feedback
```

**طلب**:

```json
{
  "recommendation_id": "rec_channels_123456",
  "feedback": {
    "rating": 4,
    "is_implemented": true,
    "comments": "التوصية كانت مفيدة جدًا، لكن كان يمكن أن تكون أكثر تفصيلاً",
    "results": {
      "impressions": 135000,
      "clicks": 4050,
      "ctr": 0.03,
      "conversions": 202,
      "roi": 2.7
    }
  }
}
```

**استجابة**:

```json
{
  "message": "تم حفظ التغذية الراجعة بنجاح",
  "feedback_id": "feedback_123456"
}
```

#### الحصول على إحصائيات التغذية الراجعة

```
GET /api/v1/learning-loop/recommendation-feedback-stats
```

**معلمات الاستعلام**:

- `campaign_id` (اختياري): معرف الحملة للتصفية
- `recommendation_type` (اختياري): نوع التوصية للتصفية (channel, budget, content)
- `time_period` (اختياري): الفترة الزمنية (last_week, last_month, last_3_months, all)

**استجابة**:

```json
{
  "stats": {
    "total_recommendations": 45,
    "feedback_received": 38,
    "average_rating": 4.2,
    "implementation_rate": 0.75,
    "effectiveness": {
      "high": 0.65,
      "medium": 0.25,
      "low": 0.1
    },
    "by_type": [
      {
        "type": "channel",
        "count": 18,
        "average_rating": 4.3,
        "implementation_rate": 0.8
      },
      {
        "type": "budget",
        "count": 15,
        "average_rating": 4.1,
        "implementation_rate": 0.73
      },
      {
        "type": "content",
        "count": 12,
        "average_rating": 4.0,
        "implementation_rate": 0.67
      }
    ],
    "trend": [
      {"month": "يناير", "average_rating": 3.8, "implementation_rate": 0.65},
      {"month": "فبراير", "average_rating": 3.9, "implementation_rate": 0.68},
      {"month": "مارس", "average_rating": 4.0, "implementation_rate": 0.7},
      {"month": "أبريل", "average_rating": 4.1, "implementation_rate": 0.72},
      {"month": "مايو", "average_rating": 4.2, "implementation_rate": 0.75},
      {"month": "يونيو", "average_rating": 4.3, "implementation_rate": 0.78}
    ]
  }
}
```

## رموز الخطأ

| الرمز | الوصف |
|------|------|
| 400 | طلب غير صالح |
| 401 | غير مصرح |
| 403 | محظور |
| 404 | غير موجود |
| 422 | خطأ في التحقق من البيانات |
| 429 | طلبات كثيرة جدًا |
| 500 | خطأ داخلي في الخادم |

## ملاحظات إضافية

- جميع الطلبات والاستجابات يجب أن تكون بتنسيق JSON.
- جميع التواريخ والأوقات بتنسيق ISO 8601 (مثال: `2023-06-01T12:00:00Z`).
- يتم تطبيق حد للطلبات بمعدل 100 طلب لكل دقيقة لكل مستخدم.
- للحصول على أحدث توثيق، راجع واجهة Swagger على `http://localhost:8000/docs`.

## الترخيص

جميع الحقوق محفوظة © 2023 Maestro AI Marketing Platform
