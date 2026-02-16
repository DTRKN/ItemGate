from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class CatalogItemBase(BaseModel):
    """Базовая схема товара из каталога"""
    id_item: str
    uid: Optional[str] = None
    sid: Optional[str] = None
    name: str
    slug: str
    stuff: Optional[str] = None
    category_id: Optional[str] = None
    photoUrl: Optional[str] = None
    image_title: Optional[str] = None
    raw_description: Optional[str] = None
    price: float
    balance: int = 0


class CatalogItemCreate(CatalogItemBase):
    """Схема для создания товара в каталоге"""
    pass


class CatalogItemView(CatalogItemBase):
    """Схема для отображения товара из каталога"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class UserGenerationBase(BaseModel):
    """Базовая схема AI-генерации"""
    generation_name: str = "Основной вариант"
    ai_description: Optional[str] = None
    ai_keywords: Optional[str] = None
    ai_prompt_version: Optional[str] = None


class UserGenerationCreate(BaseModel):
    """Схема для создания генерации"""
    catalog_item_id: int
    generation_name: str = "Основной вариант"


class UserGenerationUpdate(BaseModel):
    """Схема для обновления генерации"""
    generation_name: Optional[str] = None
    ai_description: Optional[str] = None
    ai_keywords: Optional[str] = None


class UserGenerationView(UserGenerationBase):
    """Схема для отображения генерации с данными о товаре"""
    id: int
    user_id: int
    catalog_item_id: int
    excel_exported: str
    export_count: int
    created_at: datetime
    updated_at: datetime
    
    # Вложенные данные товара
    catalog_item: Optional[CatalogItemView] = None
    
    model_config = ConfigDict(from_attributes=True)


class UserGenerationWithItem(UserGenerationView):
    """Расширенная схема с полной информацией о товаре"""
    # Дублируем поля товара на верхний уровень для удобства фронтенда
    item_name: Optional[str] = None
    item_price: Optional[float] = None
    item_photoUrl: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)
