# دليل تثبيت وتشغيل منصة Maestro

هذا الدليل يشرح خطوات تثبيت وتشغيل منصة Maestro للتسويق الرقمي المدعومة بالذكاء الاصطناعي بشكل مفصل.

## المتطلبات الأساسية

قبل البدء، تأكد من تثبيت البرامج التالية على نظامك:

1. **Git**: لاستنساخ المستودع
2. **Python 3.8+**: للواجهة الخلفية
3. **Node.js 16+**: للواجهة الأمامية
4. **PostgreSQL 12+**: لقاعدة البيانات
5. **pnpm** (موصى به) أو **npm** أو **yarn**: لإدارة حزم JavaScript

## استنساخ المشروع

```bash
git clone https://github.com/your-username/maestro-project.git
cd maestro-project
```

## إعداد الواجهة الخلفية (Backend)

### 1. إنشاء بيئة Python افتراضية

```bash
cd backend

# إنشاء بيئة افتراضية
python -m venv venv

# تفعيل البيئة الافتراضية
# على Linux/Mac:
source venv/bin/activate
# على Windows:
venv\Scripts\activate
```

### 2. تثبيت الاعتماديات

```bash
pip install -r requirements.txt
```

### 3. إعداد قاعدة البيانات

قم بإنشاء قاعدة بيانات PostgreSQL جديدة:

```bash
# الدخول إلى PostgreSQL
psql -U postgres

# إنشاء قاعدة بيانات جديدة
CREATE DATABASE maestro;

# إنشاء مستخدم جديد (اختياري)
CREATE USER maestro_user WITH PASSWORD 'your_password';

# منح الصلاحيات
GRANT ALL PRIVILEGES ON DATABASE maestro TO maestro_user;

# الخروج من PostgreSQL
\q
```

### 4. إعداد متغيرات البيئة

قم بإنشاء ملف `.env` في مجلد `backend` مع المتغيرات التالية:

```
DATABASE_URL=postgresql://maestro_user:your_password@localhost/maestro
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
OPENAI_API_KEY=your_openai_api_key  # إذا كنت تستخدم OpenAI API
```

يمكنك توليد مفتاح سري عشوائي باستخدام Python:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 5. تهيئة قاعدة البيانات

```bash
# قم بتشغيل سكريبت تهيئة قاعدة البيانات
python -m app.db.init_db
```

### 6. تشغيل الخادم

```bash
# تشغيل الخادم مع وضع إعادة التحميل التلقائي
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

سيتم تشغيل الخادم على المنفذ 8000. يمكنك الوصول إلى واجهة Swagger على الرابط:

```
http://localhost:8000/docs
```

## إعداد الواجهة الأمامية (Frontend)

### 1. تثبيت الاعتماديات

```bash
cd frontend

# باستخدام pnpm (موصى به)
pnpm install

# أو باستخدام npm
npm install

# أو باستخدام yarn
yarn install
```

### 2. إعداد متغيرات البيئة

قم بإنشاء ملف `.env` في مجلد `frontend` مع المتغيرات التالية:

```
VITE_API_URL=http://localhost:8000/api/v1
```

### 3. تشغيل خادم التطوير

```bash
# باستخدام pnpm
pnpm run dev

# أو باستخدام npm
npm run dev

# أو باستخدام yarn
yarn dev
```

سيتم تشغيل التطبيق على المنفذ 5173 بشكل افتراضي. يمكنك الوصول إليه على الرابط:

```
http://localhost:5173
```

## البناء للإنتاج

### بناء الواجهة الخلفية

لا يلزم بناء الواجهة الخلفية بشكل منفصل، ولكن يمكنك استخدام Gunicorn لتشغيل التطبيق في بيئة الإنتاج:

```bash
cd backend
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```

### بناء الواجهة الأمامية

```bash
cd frontend

# باستخدام pnpm
pnpm run build

# أو باستخدام npm
npm run build

# أو باستخدام yarn
yarn build
```

سيتم إنشاء الملفات المبنية في مجلد `dist/`. يمكنك استضافة هذه الملفات على أي خادم ويب ثابت مثل Nginx أو Apache.

## نشر التطبيق باستخدام Docker

### 1. بناء صور Docker

```bash
# بناء صورة الواجهة الخلفية
docker build -t maestro-backend -f backend/Dockerfile .

# بناء صورة الواجهة الأمامية
docker build -t maestro-frontend -f frontend/Dockerfile .
```

### 2. تشغيل الحاويات

```bash
# تشغيل قاعدة البيانات
docker run -d --name maestro-db \
  -e POSTGRES_USER=maestro_user \
  -e POSTGRES_PASSWORD=your_password \
  -e POSTGRES_DB=maestro \
  -p 5432:5432 \
  postgres:13

# تشغيل الواجهة الخلفية
docker run -d --name maestro-backend \
  -e DATABASE_URL=postgresql://maestro_user:your_password@maestro-db/maestro \
  -e SECRET_KEY=your_secret_key_here \
  -e ALGORITHM=HS256 \
  -e ACCESS_TOKEN_EXPIRE_MINUTES=30 \
  -p 8000:8000 \
  --link maestro-db \
  maestro-backend

# تشغيل الواجهة الأمامية
docker run -d --name maestro-frontend \
  -e VITE_API_URL=http://localhost:8000/api/v1 \
  -p 80:80 \
  maestro-frontend
```

## استكشاف الأخطاء وإصلاحها

### مشاكل الواجهة الخلفية

1. **خطأ في الاتصال بقاعدة البيانات**:
   - تأكد من تشغيل خدمة PostgreSQL
   - تحقق من صحة بيانات الاتصال في ملف `.env`
   - تأكد من وجود قاعدة البيانات وصلاحيات المستخدم

2. **خطأ في تثبيت الحزم**:
   - تأكد من استخدام Python 3.8 أو أحدث
   - جرب تحديث pip: `pip install --upgrade pip`
   - قم بتثبيت الحزم واحدة تلو الأخرى لتحديد الحزمة المسببة للمشكلة

3. **خطأ في تشغيل الخادم**:
   - تأكد من تفعيل البيئة الافتراضية
   - تحقق من سجلات الخطأ للحصول على تفاصيل أكثر

### مشاكل الواجهة الأمامية

1. **خطأ في تثبيت الحزم**:
   - حذف مجلد `node_modules` وملف `package-lock.json` أو `pnpm-lock.yaml` وإعادة التثبيت
   - تأكد من استخدام Node.js 16 أو أحدث

2. **خطأ في الاتصال بالواجهة الخلفية**:
   - تأكد من تشغيل خادم الواجهة الخلفية
   - تحقق من صحة عنوان API في ملف `.env`
   - تأكد من تكوين CORS بشكل صحيح في الواجهة الخلفية

3. **مشاكل في العرض أو التصميم**:
   - تأكد من تحميل جميع ملفات CSS بشكل صحيح
   - افتح وحدة تحكم المتصفح للتحقق من وجود أخطاء JavaScript

## الدعم والمساعدة

إذا واجهت أي مشاكل أو كانت لديك أسئلة، يرجى:

1. مراجعة قسم المشكلات (Issues) في مستودع GitHub
2. إنشاء مشكلة جديدة مع وصف تفصيلي للمشكلة
3. التواصل مع فريق الدعم على support@maestro-ai.com

## الترخيص

جميع الحقوق محفوظة © 2023 Maestro AI Marketing Platform
