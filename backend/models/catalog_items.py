from sqlalchemy import Column, String, Float, Integer, Text
from .base import BaseModel


class CatalogItem(BaseModel):
    """
    Общий каталог товаров из Sima-Land.
    Загружается ОДИН раз админом, используется всеми пользователями.
    """
    __tablename__ = "catalog_items"

    # Идентификаторы из Sima-Land API
    id_item = Column(String(36), unique=True, nullable=False, index=True)
    uid = Column(String(36))
    sid = Column(String(36))
    
    # Основная информация о товаре
    name = Column(String(300), nullable=False, index=True)
    slug = Column(String(200), nullable=False, index=True)
    stuff = Column(String(100))
    category_id = Column(String(36))
    
    # Медиа и описание
    photoUrl = Column(String(500))
    image_title = Column(String(150))
    raw_description = Column(Text)
    
    # Коммерческие данные
    price = Column(Float, nullable=False)
    balance = Column(Integer, default=0)
    
    def __repr__(self):
        return f"<CatalogItem(id_item={self.id_item}, name={self.name})>"
