# Maestro Backend

الواجهة الخلفية لمنصة Maestro للتسويق الرقمي المدعومة بالذكاء الاصطناعي.

## نظرة عامة

تتكون الواجهة الخلفية من خمسة مكونات رئيسية:

1. **العقل الاستراتيجي (Strategic Mind)**: قاعدة معرفة ديناميكية ومحرك استدلال هجين
2. **الشرارة الإبداعية (Creative Spark)**: توليد النصوص الإعلانية، اقتراحات بصرية، وتحليل الاتجاهات
3. **المرشد الشفاف (Transparent Mentor)**: تفسير القرارات وعرض مسارات القرار والسيناريوهات البديلة
4. **حلقة التعلم التشاركي (Collaborative Learning Loop)**: تحسين النماذج وقاعدة المعرفة بناءً على تفاعلات المستخدم
5. **قمرة القيادة التفاعلية (Interactive Cockpit)**: واجهة برمجة التطبيقات (API) لإدارة الحملات التسويقية ومراقبة الأداء

## المتطلبات

- Python 3.8+
- FastAPI
- SQLAlchemy
- PyKnow
- scikit-learn
- SHAP/LIME
- spaCy/NLTK
- وغيرها من المكتبات المذكورة في ملف `requirements.txt`

## التثبيت

1. إنشاء بيئة افتراضية:

```bash
python -m venv venv
source venv/bin/activate  # على Linux/macOS
venv\Scripts\activate  # على Windows
```

2. تثبيت المتطلبات:

```bash
pip install -r requirements.txt
```

3. إعداد ملف البيئة:

قم بإنشاء ملف `.env` في المجلد الرئيسي للمشروع وأضف المتغيرات التالية:

```
DATABASE_URL=sqlite:///./maestro.db
SECRET_KEY=your-secret-key-here
OPENAI_API_KEY=your-openai-api-key
```

## التشغيل

لتشغيل الخادم المحلي:

```bash
uvicorn app.main:app --reload
```

سيتم تشغيل الخادم على المنفذ 8000 بشكل افتراضي. يمكنك الوصول إلى واجهة Swagger على الرابط:

```
http://localhost:8000/docs
```

## هيكل المشروع

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py               # نقطة الدخول الرئيسية للتطبيق
│   ├── config.py             # إعدادات التطبيق
│   ├── database.py           # إعداد قاعدة البيانات
│   ├── models/               # نماذج قاعدة البيانات
│   ├── schemas/              # مخططات Pydantic
│   ├── api/                  # واجهات API
│   │   ├── endpoints/        # نقاط النهاية لـ API
│   ├── core/                 # المكونات الأساسية
│   │   ├── strategic_mind/   # العقل الاستراتيجي
│   │   ├── creative_spark/   # الشرارة الإبداعية
│   │   ├── transparent_mentor/ # المرشد الشفاف
│   │   └── learning_loop/    # حلقة التعلم
│   └── utils/                # أدوات مساعدة
├── tests/                    # اختبارات
├── requirements.txt          # متطلبات Python
└── README.md                 # هذا الملف
```

## واجهة برمجة التطبيقات (API)

### المستخدمين

- `POST /api/v1/users/`: إنشاء مستخدم جديد
- `POST /api/v1/users/login`: تسجيل الدخول
- `GET /api/v1/users/me`: الحصول على المستخدم الحالي
- `PUT /api/v1/users/me`: تحديث المستخدم الحالي

### الحملات

- `GET /api/v1/campaigns/`: الحصول على قائمة الحملات
- `POST /api/v1/campaigns/`: إنشاء حملة جديدة
- `GET /api/v1/campaigns/{campaign_id}`: الحصول على حملة محددة
- `PUT /api/v1/campaigns/{campaign_id}`: تحديث حملة
- `DELETE /api/v1/campaigns/{campaign_id}`: حذف حملة

### العقل الاستراتيجي

- `POST /api/v1/strategic-mind/predict-ctr`: التنبؤ بمعدل النقر إلى الظهور
- `POST /api/v1/strategic-mind/predict-roi`: التنبؤ بالعائد على الاستثمار
- `POST /api/v1/strategic-mind/recommend-channels`: توصية بقنوات التسويق

### الشرارة الإبداعية

- `POST /api/v1/creative-spark/generate-ad-copy`: توليد نص إعلاني
- `POST /api/v1/creative-spark/generate-visual-suggestions`: توليد اقتراحات بصرية
- `POST /api/v1/creative-spark/analyze-trends`: تحليل الاتجاهات

### المرشد الشفاف

- `POST /api/v1/transparent-mentor/explain-prediction`: تفسير تنبؤ
- `POST /api/v1/transparent-mentor/explain-recommendation`: تفسير توصية
- `POST /api/v1/transparent-mentor/generate-alternative-scenarios`: توليد سيناريوهات بديلة

### حلقة التعلم

- `POST /api/v1/learning-loop/save-recommendation-feedback`: حفظ التغذية الراجعة على توصية
- `GET /api/v1/learning-loop/recommendation-feedback-stats`: الحصول على إحصائيات التغذية الراجعة
- `POST /api/v1/learning-loop/update-model`: تحديث نموذج التعلم الآلي

## الترخيص

جميع الحقوق محفوظة © 2023 Maestro AI Marketing Platform
