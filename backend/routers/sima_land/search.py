from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, func
from sqlalchemy.orm import selectinload
import logging
import re

from services.database import get_db
from schemas.catalog import CatalogItemView
from models.catalog_items import CatalogItem
from models.user_generations import UserGeneration
from models.users import User
from services.auth import get_current_active_user

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/search_item_to_word/{word}", response_model=list[dict])
async def search_catalog_items(
    word: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> list:
    """
    Поиск товаров в ОБЩЕМ КАТАЛОГЕ по ключевому слову с флагом generated.
    Ищет в названии товара (name) и slug.
    """
    
    # Экранируем ввод пользователя, используем границы слова (без спец-символов)
    escaped = f"%{word}%"
    logger.info("[SEARCH_CATALOG] Поиск по слову: '%s', regex паттерн: '%s'", word, escaped)
    
    stmt = select(CatalogItem).where(
            CatalogItem.name.ilike(escaped)
    ).limit(100)



    result = await db.execute(stmt)
    items = result.scalars().all()

    print(items)
    
    logger.info("[SEARCH_CATALOG] Найдено товаров: %d", len(items))
    if items:
        for item in items[:5]:  # Логируем первые 5
            logger.debug("[SEARCH_CATALOG] Товар: id=%s, name='%s', slug='%s'", item.id, item.name, item.slug)
    
    if not items:
        logger.warning("[SEARCH_CATALOG] Слово '%s' не найдено в каталоге", word)
        return []
    
    # Получаем список catalog_item_id для которых у пользователя есть генерации
    stmt_generated = select(UserGeneration.catalog_item_id).where(
        UserGeneration.user_id == current_user.id
    )
    result_generated = await db.execute(stmt_generated)
    generated_ids = set(result_generated.scalars().all())
    
    # Формируем ответ с флагом generated
    items_with_flag = []
    for item in items:
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
            "updated_at": item.updated_at,
            "generated": item.id in generated_ids
        }
        items_with_flag.append(item_dict)
    
    return items_with_flag


@router.post("/search_generated_items/{word}", response_model=list[dict])
async def search_generated_items(
    word: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> list:
    """
    Поиск товаров, которые уже сгенерированы текущим пользователем.
    Возвращает список `UserGeneration` с вложенным `catalog_item`.
    """

    # Экранируем ввод пользователя, используем границы слова
    escaped = re.escape(word.lower())
    logger.info("[SEARCH_GENERATED] Поиск по слову: '%s', user_id=%s, regex паттерн: '%s'", word, current_user.id, escaped)

    stmt = (
        select(UserGeneration)
        .join(CatalogItem, UserGeneration.catalog_item)
        .where(
            UserGeneration.user_id == current_user.id,
            or_(
                CatalogItem.name.regexp_match(escaped, flags='i'),
            )

        )
        .options(selectinload(UserGeneration.catalog_item))
        .limit(200)
    )

    result = await db.execute(stmt)
    gens = result.scalars().all()

    logger.info("[SEARCH_GENERATED] Найдено генераций: %d", len(gens))
    if gens:
        for gen in gens[:5]:  # Логируем первые 5
            item_name = gen.catalog_item.name if gen.catalog_item else "УДАЛЁН"
            logger.debug("[SEARCH_GENERATED] Генерация: id=%s, item_name='%s'", gen.id, item_name)

    if not gens:
        logger.warning("[SEARCH_GENERATED] Ничего не найдено для user_id=%s", current_user.id)
        return []

    out = []
    for gen in gens:
        ci = gen.catalog_item
        
        # Защита от удалённого товара
        if ci is None:
            catalog_item_data = {
                "id": None,
                "id_item": None,
                "name": "ТОВАР УДАЛЁН",
                "slug": "",
                "price": 0,
                "photoUrl": "",
                "category_id": None,
                "stuff": None,
                "raw_description": None,
            }
        else:
            catalog_item_data = {
                "id": ci.id,
                "id_item": ci.id_item,
                "name": ci.name,
                "slug": ci.slug,
                "price": ci.price,
                "photoUrl": ci.photoUrl,
                "category_id": ci.category_id,
                "stuff": ci.stuff,
                "raw_description": ci.raw_description,
            }
        
        gen_dict = {
            "id": gen.id,
            "user_id": gen.user_id,
            "catalog_item_id": gen.catalog_item_id,
            "generation_name": gen.generation_name,
            "ai_description": gen.ai_description,
            "ai_keywords": gen.ai_keywords,
            "ai_prompt_version": gen.ai_prompt_version,
            "excel_exported": gen.excel_exported,
            "export_count": gen.export_count,
            "created_at": gen.created_at,
            "updated_at": gen.updated_at,
            "catalog_item": catalog_item_data
        }
        out.append(gen_dict)

    return out