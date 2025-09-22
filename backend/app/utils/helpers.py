from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt
import os
import re
import json

from app.config import settings


# إعداد تشفير كلمات المرور
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    التحقق من كلمة المرور
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    تشفير كلمة المرور
    """
    return pwd_context.hash(password)


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    إنشاء رمز وصول JWT
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    return encoded_jwt


def sanitize_filename(filename: str) -> str:
    """
    تنظيف اسم الملف من الأحرف غير الآمنة
    """
    # إزالة الأحرف غير الآمنة
    sanitized = re.sub(r'[^\w\s.-]', '', filename)
    # استبدال المسافات بالشرطات السفلية
    sanitized = re.sub(r'\s+', '_', sanitized)
    return sanitized


def ensure_dir(directory: str) -> None:
    """
    التأكد من وجود المجلد
    """
    if not os.path.exists(directory):
        os.makedirs(directory)


def load_json_file(file_path: str) -> Dict[str, Any]:
    """
    تحميل ملف JSON
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading JSON file {file_path}: {e}")
        return {}


def save_json_file(data: Dict[str, Any], file_path: str) -> bool:
    """
    حفظ بيانات في ملف JSON
    """
    try:
        # التأكد من وجود المجلد
        directory = os.path.dirname(file_path)
        ensure_dir(directory)
        
        # حفظ البيانات
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        return True
    except Exception as e:
        print(f"Error saving JSON file {file_path}: {e}")
        return False


def format_date(date: datetime, format_str: str = "%Y-%m-%d") -> str:
    """
    تنسيق التاريخ
    """
    return date.strftime(format_str)


def parse_date(date_str: str, format_str: str = "%Y-%m-%d") -> Optional[datetime]:
    """
    تحليل التاريخ من نص
    """
    try:
        return datetime.strptime(date_str, format_str)
    except ValueError:
        return None


def calculate_date_diff(start_date: datetime, end_date: datetime) -> int:
    """
    حساب الفرق بين تاريخين بالأيام
    """
    return (end_date - start_date).days


def truncate_text(text: str, max_length: int = 100) -> str:
    """
    اقتصاص النص إلى طول محدد
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."
