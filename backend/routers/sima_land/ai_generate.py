from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import logging

from services.database import get_db
from schemas.catalog import UserGenerationCreate
from models.catalog_items import CatalogItem
from models.user_generations import UserGeneration
from models.log import Log
from models.users import User
from services.ai_client import openRouterClient
from services.prompt_manager import prompt_manager
from services.auth import get_current_active_user
from config import config as conf

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/ai_generate_desc_seller/{catalog_item_id}")
async def generate_ai_description(
    catalog_item_id: int,
    generation_name: str = "Основной вариант",
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> dict:
    """
    Генерирует AI описание для товара из каталога.
    Создаёт новую генерацию или обновляет существующую с тем же именем.
    """
    
    logger.info("[AI_GENERATE] Запрос от user_id=%s для catalog_item_id=%s, generation_name='%s'", 
                current_user.id, catalog_item_id, generation_name)
    
    # Получаем товар из каталога
    stmt = select(CatalogItem).where(CatalogItem.id == catalog_item_id)
    result = await db.execute(stmt)
    catalog_item = result.scalar_one_or_none()
    
    if not catalog_item:
        logger.error("[AI_GENERATE] Товар с ID %s не найден в каталоге", catalog_item_id)
        raise HTTPException(status_code=404, detail=f"Товар с ID {catalog_item_id} не найден в каталоге")
    
    logger.info("[AI_GENERATE] Товар найден: name='%s', id_item=%s", catalog_item.name, catalog_item.id_item)
    
    # Формируем запрос для AI
    request_item = f"""
        Название товара: {catalog_item.name},
        Материал: {catalog_item.stuff or "не указан"},
        Описание дополнительное: {catalog_item.image_title or "отсутствует"},
        Цена: {catalog_item.price},
    """
    
    print(f'ТОВАР для генерации: {catalog_item.name}')
    logger.debug("[AI_GENERATE] Отправляем запрос к AI с данными товара")

    try:
        ai_response = await openRouterClient.get_response(user_data=str(request_item))
        response = ai_response.model_dump()
        logger.info("[AI_GENERATE] Получен ответ от AI")
    except HTTPException as e:
        detail = str(e.detail) if hasattr(e, 'detail') else str(e)
        log = Log(
            user_id=current_user.id,
            action='generate_error',
            item_id=catalog_item.id,
            message=f"Ошибка генерации AI: {detail}",
            status='error'
        )
        db.add(log)
        await db.commit()
        raise
    except Exception as e:
        # Логируем ошибку
        log = Log(
            user_id=current_user.id,
            action='generate_error',
            item_id=catalog_item.id,
            message=f"Ошибка генерации AI: {str(e)}",
            status='error'
        )
        db.add(log)
        await db.commit()
        raise HTTPException(status_code=500, detail=f"Ошибка генерации AI: {str(e)}")

    logger.debug("[AI_GENERATE] Данные от ИИ получены, сохраняем генерацию")
    print("Данные от ИИ получены, сохраняем генерацию")
    
    prompt_version = await prompt_manager.load_system_prompt(conf.prompt_system_generate_info)
    
    # Проверяем, есть ли уже генерация с таким именем для этого товара
    stmt = select(UserGeneration).where(
        UserGeneration.user_id == current_user.id,
        UserGeneration.catalog_item_id == catalog_item.id,
        UserGeneration.generation_name == generation_name
    )
    result = await db.execute(stmt)
    existing_generation = result.scalar_one_or_none()
    
    logger.debug("[AI_GENERATE] Проверка существующей генерации: %s", 
                "найдена" if existing_generation else "не найдена")
    
    if existing_generation:
        # Обновляем существующую генерацию
        existing_generation.ai_description = str(response.get("Description", ""))
        existing_generation.ai_keywords = str(response.get("Words", ""))
        existing_generation.ai_prompt_version = str(prompt_version['version'])
        await db.commit()
        await db.refresh(existing_generation)
        
        logger.info("[AI_GENERATE] Генерация ОБНОВЛЕНА: generation_id=%s, user_id=%s, catalog_item_id=%s",
                   existing_generation.id, current_user.id, catalog_item.id)
        
        generation_id = existing_generation.id
        generation_obj = existing_generation
        message = f"Генерация обновлена: {catalog_item.name} (вариант: {generation_name})"
    else:
        # Создаём новую генерацию
        new_generation = UserGeneration(
            user_id=current_user.id,
            catalog_item_id=catalog_item.id,
            generation_name=generation_name,
            ai_description=str(response.get("Description", "")),
            ai_keywords=str(response.get("Words", "")),
            ai_prompt_version=str(prompt_version['version'])
        )
        db.add(new_generation)
        await db.commit()
        await db.refresh(new_generation)
        
        logger.info("[AI_GENERATE] Генерация СОЗДАНА: generation_id=%s, user_id=%s, catalog_item_id=%s",
                   new_generation.id, current_user.id, catalog_item.id)
        
        generation_id = new_generation.id
        generation_obj = new_generation
        message = f"Генерация создана: {catalog_item.name} (вариант: {generation_name})"
    
    # Логируем успешную генерацию
    log = Log(
        user_id=current_user.id,
        action='generate',
        item_id=catalog_item.id_item,
        message=message,
        status='completed'
    )
    db.add(log)
    await db.commit()
    
    # Загружаем связанный каталожный товар для возврата полных данных
    await db.refresh(generation_obj, ['catalog_item'])
    
    result_data = {
        "success": True,
        "generation_id": generation_id,
        "catalog_item_id": catalog_item.id,
        "message": message,
        "generation": {
            "id": generation_obj.id,
            "ai_description": generation_obj.ai_description,
            "ai_keywords": generation_obj.ai_keywords,
            "catalog_item": {
                "id": catalog_item.id,
                "id_item": catalog_item.id_item,
                "name": catalog_item.name,
                "photoUrl": catalog_item.photoUrl,
                "price": catalog_item.price
            }
        }
    }
    
    logger.info("[AI_GENERATE] Возвращаем результат: generation_id=%s, success=True", generation_id)
    logger.debug("[AI_GENERATE] Детали: catalog_item.name='%s', user_id=%s", catalog_item.name, current_user.id)
    
    return result_data