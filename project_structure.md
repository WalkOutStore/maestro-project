# هيكل مشروع Maestro

## نظرة عامة

مشروع Maestro هو منصة للتسويق الرقمي مدعومة بالذكاء الاصطناعي، تجمع بين التحليل الاستراتيجي والإبداع والشفافية. يتكون المشروع من خمسة مكونات رئيسية:

1. **العقل الاستراتيجي (Strategic Mind)**: قاعدة معرفة ديناميكية ومحرك استدلال هجين
2. **الشرارة الإبداعية (Creative Spark)**: توليد النصوص الإعلانية، اقتراحات بصرية، وتحليل الاتجاهات
3. **المرشد الشفاف (Transparent Mentor)**: تفسير القرارات وعرض مسارات القرار والسيناريوهات البديلة
4. **حلقة التعلم التشاركي (Collaborative Learning Loop)**: تحسين النماذج وقاعدة المعرفة بناءً على تفاعلات المستخدم
5. **قمرة القيادة التفاعلية (Interactive Cockpit)**: واجهة مستخدم تفاعلية لإدارة الحملات التسويقية ومراقبة الأداء

## هيكل المشروع

```
maestro-project/
│
├── backend/                      # الواجهة الخلفية (FastAPI)
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py               # نقطة الدخول الرئيسية للتطبيق
│   │   ├── config.py             # إعدادات التطبيق
│   │   ├── database.py           # إعداد قاعدة البيانات
│   │   ├── models/               # نماذج قاعدة البيانات
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── campaign.py
│   │   │   └── knowledge_base.py
│   │   ├── schemas/              # مخططات Pydantic
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── campaign.py
│   │   │   └── knowledge_base.py
│   │   ├── api/                  # واجهات API
│   │   │   ├── __init__.py
│   │   │   ├── endpoints/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── users.py
│   │   │   │   ├── campaigns.py
│   │   │   │   ├── strategic_mind.py
│   │   │   │   ├── creative_spark.py
│   │   │   │   ├── transparent_mentor.py
│   │   │   │   └── learning_loop.py
│   │   │   └── api.py
│   │   ├── core/                 # المكونات الأساسية
│   │   │   ├── __init__.py
│   │   │   ├── strategic_mind/    # العقل الاستراتيجي
│   │   │   │   ├── __init__.py
│   │   │   │   ├── knowledge_base.py
│   │   │   │   └── inference_engine.py
│   │   │   ├── creative_spark/    # الشرارة الإبداعية
│   │   │   │   ├── __init__.py
│   │   │   │   ├── text_generator.py
│   │   │   │   ├── visual_suggestions.py
│   │   │   │   └── trend_analyzer.py
│   │   │   ├── transparent_mentor/ # المرشد الشفاف
│   │   │   │   ├── __init__.py
│   │   │   │   ├── explainer.py
│   │   │   │   └── visualizer.py
│   │   │   └── learning_loop/     # حلقة التعلم
│   │   │       ├── __init__.py
│   │   │       ├── feedback.py
│   │   │       └── model_updater.py
│   │   └── utils/                # أدوات مساعدة
│   │       ├── __init__.py
│   │       └── helpers.py
│   ├── tests/                    # اختبارات
│   │   ├── __init__.py
│   │   ├── test_api.py
│   │   └── test_core.py
│   ├── requirements.txt          # متطلبات Python
│   └── README.md                 # توثيق الواجهة الخلفية
│
├── frontend/                     # الواجهة الأمامية (React)
│   ├── public/
│   │   ├── index.html
│   │   ├── favicon.ico
│   │   └── assets/
│   ├── src/
│   │   ├── index.js              # نقطة الدخول الرئيسية
│   │   ├── App.js                # مكون التطبيق الرئيسي
│   │   ├── components/           # مكونات واجهة المستخدم
│   │   │   ├── common/           # مكونات مشتركة
│   │   │   │   ├── Header.js
│   │   │   │   ├── Sidebar.js
│   │   │   │   └── Footer.js
│   │   │   ├── dashboard/        # مكونات لوحة التحكم
│   │   │   │   ├── Dashboard.js
│   │   │   │   ├── PerformanceMetrics.js
│   │   │   │   └── CampaignAnalytics.js
│   │   │   ├── strategic_mind/   # مكونات العقل الاستراتيجي
│   │   │   │   └── StrategicMind.js
│   │   │   ├── creative_spark/   # مكونات الشرارة الإبداعية
│   │   │   │   ├── CreativeSpark.js
│   │   │   │   ├── TextGenerator.js
│   │   │   │   └── TrendAnalyzer.js
│   │   │   ├── transparent_mentor/ # مكونات المرشد الشفاف
│   │   │   │   ├── TransparentMentor.js
│   │   │   │   └── DecisionExplainer.js
│   │   │   ├── learning_loop/    # مكونات حلقة التعلم
│   │   │   │   ├── LearningLoop.js
│   │   │   │   └── FeedbackForm.js
│   │   │   └── sandbox/          # مكونات وضع الاختبار
│   │   │       └── Sandbox.js
│   │   ├── pages/                # صفحات التطبيق
│   │   │   ├── Home.js
│   │   │   ├── Login.js
│   │   │   ├── Campaigns.js
│   │   │   └── Settings.js
│   │   ├── services/             # خدمات API
│   │   │   ├── api.js
│   │   │   ├── auth.js
│   │   │   └── campaigns.js
│   │   ├── utils/                # أدوات مساعدة
│   │   │   ├── helpers.js
│   │   │   └── constants.js
│   │   ├── hooks/                # React hooks مخصصة
│   │   │   └── useApi.js
│   │   ├── context/              # React context
│   │   │   └── AuthContext.js
│   │   ├── styles/               # ملفات CSS
│   │   │   ├── index.css
│   │   │   └── theme.js
│   │   └── assets/               # موارد (صور، أيقونات)
│   │       └── images/
│   ├── package.json
│   └── README.md                 # توثيق الواجهة الأمامية
│
└── README.md                     # توثيق المشروع الرئيسي
```

## التقنيات المستخدمة

### الواجهة الخلفية (Backend)
- **لغة البرمجة**: Python
- **إطار العمل**: FastAPI
- **قاعدة البيانات**: PostgreSQL/SQLite
- **مكتبات الذكاء الاصطناعي**: 
  - PyKnow (للقواعد الرمزية)
  - scikit-learn / XGBoost (لنماذج التعلم الآلي)
  - HuggingFace Transformers / OpenAI API (لتوليد النصوص)
  - SHAP / LIME (لتفسير النماذج)
  - spaCy / NLTK (لمعالجة اللغة الطبيعية)

### الواجهة الأمامية (Frontend)
- **لغة البرمجة**: JavaScript
- **إطار العمل**: React
- **مكتبة واجهة المستخدم**: Material-UI (MUI)
- **مكتبات الرسوم البيانية**: Recharts / Chart.js
- **إدارة الحالة**: React Context API
- **أدوات البناء**: Vite
