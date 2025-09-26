@echo off
REM تفعيل البيئة الافتراضية
call conda activate maestro-env

REM الانتقال إلى مجلد Backend وتشغيل Uvicorn
start cmd /k "cd C:\Users\Lenovo\Downloads\maestro-project-updated\maestro-project\backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

REM الانتقال إلى مجلد Frontend وتشغيل pnpm
start cmd /k "cd C:\Users\Lenovo\Downloads\maestro-project-updated\maestro-project\frontend && pnpm install && pnpm run dev"

echo All servers are running!
pause
