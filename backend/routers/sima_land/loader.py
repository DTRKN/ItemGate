from fastapi import Depends, APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import httpx

from services.database import get_db
from schemas.catalog import CatalogItemCreate
from models.catalog_items import CatalogItem
from models.log import Log
from models.users import User
from services.auth import get_current_admin_user
from .utils import map_api_data_to_item

router = APIRouter()

@router.get("/loading_words_db/{count}")
async def func(
    count: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """Загружает товары со Sima-Land в ОБЩИЙ КАТАЛОГ с потоковой передачей прогресса (только для админов)"""
    
    async def event_generator():
        if count <= 0 or type(count) != int:  
            yield "data: Некорректное количество товаров\n\n"
            return
        
        if count >= 10000:
            yield "data: Лимит 10000 товаров\n\n"
            return

        copy_count = count
        timeout = httpx.Timeout(connect=5.0, read=30.0, write=10.0, pool=5.0)
        page_number = 1
        pagination = (count // 50) + 1
        
        yield f"data: Начинаю загрузку {count} товаров в общий каталог\n\n"

        while 0 < pagination:
            async with httpx.AsyncClient(
                base_url="https://www.sima-land.ru/api/v3",
                headers={'Content-Type': 'application/json'},
                timeout=timeout,
                follow_redirects=False
            ) as client:
                try:
                    response = await client.get(f"/item/?page={page_number}")
                    response.raise_for_status()
                    items = response.json().get("items", [])
                except httpx.HTTPError as e:
                    yield f"data: Ошибка API: {str(e)}\n\n"
                    return
                
            msg = f"Страница {page_number}: получены данные ({len(items)} товаров)"
            yield f"data: {msg}\n\n"

            for item in items:
                if copy_count <= 0:  
                    break

                try:
                    item_data = map_api_data_to_item(item)
                    catalog_item = CatalogItem(**item_data)

                    # Проверяем, есть ли уже в каталоге
                    result = await db.execute(
                        select(CatalogItem).where(CatalogItem.id_item == catalog_item.id_item).limit(1)
                    )
                    existing_item = result.scalar_one_or_none()
                    
                    if not existing_item:
                        db.add(catalog_item)
                        await db.commit()
                        await db.refresh(catalog_item)
                        
                        # Логируем успешное добавление
                        log = Log(
                            user_id=current_admin.id,
                            action='catalog_load',
                            item_id=catalog_item.id_item,
                            message=f"Товар добавлен в каталог: {catalog_item.name}",
                            status='completed'
                        )
                        db.add(log)
                        await db.commit()

                        yield f"data: ✓ Товар [{catalog_item.id_item}] добавлен в каталог | Осталось {copy_count - 1}\n\n"
                        copy_count -= 1
                    else:
                        yield f"data: ⊘ Товар [{catalog_item.id_item}] уже есть в каталоге\n\n"
                        copy_count -= 1
                except Exception as e:
                    yield f"data: ⚠ Ошибка при обработке товара: {str(e)}\n\n"
                    copy_count -= 1

            page_number += 1
            pagination -= 1

        yield "data: ✓ Загрузка в каталог завершена\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")