from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """
    المخطط الأساسي للمستخدم
    """
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    is_active: bool = True


class UserCreate(UserBase):
    """
    مخطط إنشاء مستخدم جديد
    """
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    """
    مخطط تحديث بيانات المستخدم
    """
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str] = Field(None, min_length=8)
    is_active: Optional[bool] = None


class UserInDBBase(UserBase):
    """
    مخطط المستخدم في قاعدة البيانات
    """
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    is_superuser: bool = False

    class Config:
        orm_mode = True


class User(UserInDBBase):
    """
    مخطط المستخدم للعرض
    """
    pass


class UserInDB(UserInDBBase):
    """
    مخطط المستخدم في قاعدة البيانات مع كلمة المرور المشفرة
    """
    hashed_password: str


class Token(BaseModel):
    """
    مخطط رمز الوصول
    """
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    """
    مخطط محتوى رمز الوصول
    """
    sub: Optional[int] = None
