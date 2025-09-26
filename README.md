# مشروع Maestro للتسويق الرقمي المدعوم بالذكاء الاصطناعي

![Maestro Logo](/home/ubuntu/maestro-project/frontend/src/assets/images/maestro_logo.png)

## نظرة عامة

**Maestro** هو منصة متكاملة للتسويق الرقمي مدعومة بالذكاء الاصطناعي، تجمع بين قوة التحليل الاستراتيجي والإبداع في إنشاء المحتوى والشفافية في اتخاذ القرارات والتعلم المستمر من خلال التغذية الراجعة.

تتكون المنصة من خمسة مكونات رئيسية:

1. **العقل الاستراتيجي (Strategic Mind)**: قاعدة معرفة ديناميكية ومحرك استدلال هجين يجمع بين القواعد المنطقية والتعلم الآلي لتقديم تحليلات استراتيجية وتوصيات مدروسة.

2. **الشرارة الإبداعية (Creative Spark)**: محرك إبداعي متطور يولد أفكارًا ومحتوى إبداعي يتناسب مع هوية العلامة التجارية واتجاهات السوق الحالية.

3. **المرشد الشفاف (Transparent Mentor)**: نظام تفسير متقدم يوضح القرارات والتوصيات بطريقة سهلة الفهم، مما يعزز الثقة والتعلم.

4. **حلقة التعلم التشاركي (Collaborative Learning Loop)**: نظام تعلم مستمر يستفيد من تفاعلات المستخدمين لتحسين النماذج وقاعدة المعرفة بشكل تلقائي.

5. **قمرة القيادة التفاعلية (Interactive Cockpit)**: لوحة تحكم شاملة تتيح للمستخدمين إدارة حملاتهم التسويقية ومراقبة أدائها بسهولة.

## هيكل المشروع

```
maestro-project/
├── backend/                 # الواجهة الخلفية (FastAPI)
│   ├── app/                 # تطبيق FastAPI
│   │   ├── api/             # واجهات برمجة التطبيقات (API)
│   │   ├── core/            # المكونات الأساسية للذكاء الاصطناعي
│   │   ├── models/          # نماذج قاعدة البيانات
│   │   ├── schemas/         # مخططات Pydantic
│   │   └── utils/           # أدوات مساعدة
│   ├── requirements.txt     # متطلبات Python
│   └── README.md            # توثيق الواجهة الخلفية
├── frontend/                # الواجهة الأمامية (React)
│   ├── public/              # الملفات العامة
│   ├── src/                 # مصدر التطبيق
│   │   ├── assets/          # الأصول (الصور، الأيقونات، إلخ)
│   │   ├── components/      # مكونات React
│   │   ├── contexts/        # سياقات React
│   │   ├── layouts/         # تخطيطات الصفحات
│   │   ├── pages/           # صفحات التطبيق
│   │   └── services/        # خدمات API
│   ├── package.json         # تبعيات المشروع
│   └── README.md            # توثيق الواجهة الأمامية
└── README.md                # هذا الملف
```

## المتطلبات التقنية

### الواجهة الخلفية (Backend)
- Python 3.8+
- FastAPI
- SQLAlchemy
- PostgreSQL
- scikit-learn
- TensorFlow/PyTorch (للنماذج المتقدمة)
- NLTK/spaCy (لمعالجة اللغة الطبيعية)

### الواجهة الأمامية (Frontend)
- Node.js 16+
- React 18
- React Router v6
- Tailwind CSS
- shadcn/ui
- Recharts
- Axios

## تثبيت وتشغيل المشروع

### الواجهة الخلفية (Backend)

1. إنشاء بيئة Python افتراضية:

```bash
cd backend
python -m venv venv
source venv/bin/activate  # على Linux/Mac
# أو
venv\Scripts\activate  # على Windows
```

2. تثبيت الاعتماديات:

```bash
pip install -r requirements.txt
```

3. تشغيل الخادم:

```bash
uvicorn app.main:app --reload
```

سيتم تشغيل الخادم على المنفذ 8000 بشكل افتراضي. يمكنك الوصول إلى واجهة Swagger على الرابط:

```
http://localhost:8000/docs
```

### الواجهة الأمامية (Frontend)

1. تثبيت الاعتماديات:

```bash
cd frontend
pnpm install  # أو npm install
```

2. تشغيل خادم التطوير:

```bash
pnpm run dev  # أو npm run dev
```

سيتم تشغيل التطبيق على المنفذ 5173 بشكل افتراضي. يمكنك الوصول إليه على الرابط:

```
http://localhost:5173
```

## متغيرات البيئة

### الواجهة الخلفية (Backend)

قم بإنشاء ملف `.env` في مجلد `backend` مع المتغيرات التالية:

```
DATABASE_URL=postgresql://user:password@localhost/maestro
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
OPENAI_API_KEY=your_openai_api_key  # إذا كنت تستخدم OpenAI API
```

### الواجهة الأمامية (Frontend)

قم بإنشاء ملف `.env` في مجلد `frontend` مع المتغيرات التالية:

```
VITE_API_URL=http://localhost:8000/api/v1
```

## واجهات برمجة التطبيقات (APIs)

### المستخدمين
- `POST /api/v1/users`: إنشاء مستخدم جديد
- `POST /api/v1/users/login`: تسجيل الدخول
- `GET /api/v1/users/me`: الحصول على بيانات المستخدم الحالي
- `PUT /api/v1/users/me`: تحديث بيانات المستخدم الحالي

### الحملات
- `GET /api/v1/campaigns`: الحصول على قائمة الحملات
- `POST /api/v1/campaigns`: إنشاء حملة جديدة
- `GET /api/v1/campaigns/{id}`: الحصول على تفاصيل حملة
- `PUT /api/v1/campaigns/{id}`: تحديث حملة
- `DELETE /api/v1/campaigns/{id}`: حذف حملة

### العقل الاستراتيجي
- `POST /api/v1/strategic-mind/predict-ctr`: التنبؤ بمعدل النقر إلى الظهور
- `POST /api/v1/strategic-mind/predict-roi`: التنبؤ بالعائد على الاستثمار
- `POST /api/v1/strategic-mind/recommend-channels`: توصية بقنوات التسويق

### الشرارة الإبداعية
- `POST /api/v1/creative-spark/generate-ad-copy`: توليد نص إعلاني
- `POST /api/v1/creative-spark/generate-visual-suggestions`: توليد اقتراحات بصرية
- `POST /api/v1/creative-spark/analyze-trends`: تحليل اتجاهات المحتوى

### المرشد الشفاف
- `POST /api/v1/transparent-mentor/explain-prediction`: شرح التنبؤات
- `POST /api/v1/transparent-mentor/explain-recommendation`: شرح التوصيات
- `POST /api/v1/transparent-mentor/generate-alternative-scenarios`: توليد سيناريوهات بديلة

### حلقة التعلم
- `POST /api/v1/learning-loop/save-recommendation-feedback`: حفظ التغذية الراجعة على التوصيات
- `GET /api/v1/learning-loop/recommendation-feedback-stats`: إحصائيات التغذية الراجعة

## الترخيص

جميع الحقوق محفوظة © 2025 Maestro AI Marketing Platform
