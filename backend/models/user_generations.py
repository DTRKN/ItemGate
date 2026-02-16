from sqlalchemy import Column, String, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel


class UserGeneration(BaseModel):
    """
    AI-генерации пользователей для товаров из каталога.
    Один пользователь может создать НЕСКОЛЬКО генераций для одного товара.
    """
    __tablename__ = "user_generations"

    # Связи
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    catalog_item_id = Column(Integer, ForeignKey('catalog_items.id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Название варианта генерации
    generation_name = Column(String(100), default="Основной вариант")
    
    # AI-сгенерированные данные
    ai_description = Column(Text)
    ai_keywords = Column(Text)
    ai_prompt_version = Column(String(50))
    
    # Статус экспорта
    excel_exported = Column(String(20), default='not_exported')
    export_count = Column(Integer, default=0)
    
    # Relationships
    user = relationship("User", backref="generations")
    catalog_item = relationship("CatalogItem", backref="generations")
    
    def __repr__(self):
        return f"<UserGeneration(id={self.id}, user_id={self.user_id}, item={self.catalog_item_id})>"
