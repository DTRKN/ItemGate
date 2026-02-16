from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ItemSchema(BaseModel):
    id_item: Optional[str] = Field(None, max_length=36)
    uid: Optional[str] = Field(None, max_length=36)
    sid: Optional[str] = Field(None, max_length=36)
    balance: Optional[int] = None 
    name: str = Field(..., max_length=300)
    slug: str = Field(..., max_length=200)
    stuff: Optional[str] = Field(None, max_length=100)
    category_id: Optional[str] = Field(None, max_length=36)
    photoUrl: Optional[str] = Field(None, max_length=500)
    image_title: Optional[str] = Field(None, max_length=150)
    price: float

    class Config:
        from_attributes = True

class ItemView(BaseModel):
    id_item: Optional[str] = Field(None, max_length=36)
    name: str = Field(..., max_length=300)
    stuff: Optional[str] = Field(None, max_length=100)
    photoUrl: Optional[str] = Field(None, max_length=500)
    image_title: Optional[str] = Field(None, max_length=150)
    price: float

    class Config:
        from_attributes = True
    
class ItemInfo_ai(BaseModel):
    Description: str = Field(description="Описание товара от AI")
    Words: list[str] = Field(alias="Words", description="Список ключевых слов") 
    

class ItemWithAI(BaseModel):
    id_item: Optional[str] = Field(None, max_length=36)
    name: str = Field(..., max_length=300)
    price: float
    ai_description: Optional[str] = None
    ai_keywords: Optional[str] = None
    ai_prompt_version: Optional[str] = None
    photoUrl: Optional[str] = None
    stuff: Optional[str] = None
    
    class Config:
        from_attributes = True
