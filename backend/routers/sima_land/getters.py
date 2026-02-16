from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
import logging

from services.database import get_db
from schemas.catalog import CatalogItemView, UserGenerationView
from models.catalog_items import CatalogItem
from models.user_generations import UserGeneration
from models.users import User
from services.auth import get_current_active_user

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/get_items")
async def get_catalog_items(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> list[dict]:
    """
    Получить товары из ОБЩЕГО КАТАЛОГА, которые ещё НЕ сгенерированы пользователем.
    Показывает только те товары, для которых пользователь НЕ создал описания.
    """
    logger.info("[GET_ITEMS] Запрос от user_id=%s", current_user.id)
    
    # Проверяем общее количество товаров в каталоге
    total_count_stmt = select(CatalogItem)
    total_result = await db.execute(total_count_stmt)
    total_items = total_result.scalars().all()
    logger.info("[GET_ITEMS] Всего товаров в каталоге: %d", len(total_items))
    
    # Подзапрос: список catalog_item_id для которых у пользователя УЖЕ есть генерации
    stmt_generated = select(UserGeneration.catalog_item_id).where(
        UserGeneration.user_id == current_user.id
    )

    print(UserGeneration.user_id, current_user.id)
    result_generated = await db.execute(stmt_generated)
    generated_ids = result_generated.scalars().all()
    logger.info("[GET_ITEMS] Пользователь уже сгенерировал: %d товаров", len(generated_ids))
    
    # Получаем товары, которых НЕТ в генерациях пользователя
    stmt = select(CatalogItem).where(
        CatalogItem.id.notin_(stmt_generated)
    ).order_by(CatalogItem.created_at.desc())
    
    result = await db.execute(stmt)
    catalog_items = result.scalars().all()
    
    logger.info("[GET_ITEMS] Показываем пользователю (ещё не сгенерированных): %d товаров", len(catalog_items))
    if catalog_items:
        for item in catalog_items[:3]:  # Первые 3 товара
            logger.debug("[GET_ITEMS] Товар: id=%s, name='%s'", item.id, item.name)
    
    # Формируем ответ
    items_list = []
    for item in catalog_items:
        item_dict = {
            "id": item.id,
            "id_item": item.id_item,
            "uid": item.uid,
            "sid": item.sid,
            "name": item.name,
            "slug": item.slug,
            "stuff": item.stuff,
            "category_id": item.category_id,
            "photoUrl": item.photoUrl,
            "image_title": item.image_title,
            "raw_description": item.raw_description,
            "price": item.price,
            "balance": item.balance,
            "created_at": item.created_at,
            "updated_at": item.updated_at
        }
        items_list.append(item_dict)
    
    return items_list

@router.get("/get_items_sellers")
async def get_user_generations(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> list[UserGenerationView]:
    """
    Получить AI-генерации ТЕКУЩЕГО пользователя с данными о товарах.
    Показывает только те товары, для которых пользователь создал описания.
    """
    logger.info("[GET_ITEMS_SELLERS] Запрос от user_id=%s", current_user.id)
    
    stmt = (
        select(UserGeneration)
        .where(UserGeneration.user_id == current_user.id)
        .options(selectinload(UserGeneration.catalog_item))
        .order_by(UserGeneration.created_at.desc())
    )
    result = await db.execute(stmt)
    generations = result.scalars().all()
    
    logger.info("[GET_ITEMS_SELLERS] Найдено генераций: %d", len(generations))
    if generations:
        for gen in generations[:3]:  # Первые 3
            item_name = gen.catalog_item.name if gen.catalog_item else "УДАЛЁН"
            logger.debug("[GET_ITEMS_SELLERS] Генерация: id=%s, item_name='%s'", gen.id, item_name)
    
    return generations