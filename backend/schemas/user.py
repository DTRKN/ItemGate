from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserRole:
    """Роли пользователей"""
    ADMIN = "admin"
    USER = "user"


class UserBase(BaseModel):
    """Базовая схема пользователя"""
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    """Схема для регистрации"""
    password: str = Field(..., min_length=6, description="Минимум 6 символов")


class UserLogin(BaseModel):
    """Схема для логина"""
    email: EmailStr
    password: str


class UserResponse(UserBase):
    """Схема для ответа с данными пользователя"""
    id: int
    role: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    """Схема токена"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Данные из токена"""
    email: Optional[str] = None
    role: Optional[str] = None
