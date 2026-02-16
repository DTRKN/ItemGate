from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, desc
from pydantic import BaseModel
from datetime import datetime

from services.database import get_db
from models.user_generations import UserGeneration
from models.log import Log
from models.users import User
from schemas.log import LogResponse
from services.auth import get_current_admin_user, get_current_active_user

router = APIRouter()


@router.put('/update_generation/{generation_id}')
async def update_generation(
    generation_id: int,
    payload: dict,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Обновляет AI-генерацию пользователя.
    Можно обновить: generation_name, ai_description, ai_keywords
    """
    # Проверяем, что генерация принадлежит текущему пользователю
    stmt = select(UserGeneration).where(
        UserGeneration.id == generation_id,
        UserGeneration.user_id == current_user.id
    )
    result = await db.execute(stmt)
    generation = result.scalar_one_or_none()
    
    if not generation:
        raise HTTPException(status_code=404, detail='Генерация не найдена или не принадлежит вам')
    
    # Обновляем только разрешённые поля
    allowed_fields = ['generation_name', 'ai_description', 'ai_keywords']
    update_data = {k: v for k, v in payload.items() if k in allowed_fields}
    
    if not update_data:
        raise HTTPException(status_code=400, detail='Нет полей для обновления')
    
    stmt = update(UserGeneration).where(
        UserGeneration.id == generation_id
    ).values(**update_data)
    await db.execute(stmt)
    await db.commit()

    # Получаем обновлённую генерацию
    result = await db.execute(select(UserGeneration).where(UserGeneration.id == generation_id))
    updated_generation = result.scalars().first()
    
    # Логируем обновление
    log = Log(
        user_id=current_user.id,
        action='update_generation',
        item_id=str(generation_id),
        message=f"Обновлены поля генерации: {', '.join(update_data.keys())}",
        status='completed'
    )
    db.add(log)
    await db.commit()
    
    return updated_generation


@router.delete('/delete_generation/{generation_id}')
async def delete_generation(
    generation_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Удаляет AI-генерацию пользователя"""
    # Проверяем владельца
    stmt = select(UserGeneration).where(
        UserGeneration.id == generation_id,
        UserGeneration.user_id == current_user.id
    )
    result = await db.execute(stmt)
    generation = result.scalar_one_or_none()
    
    if not generation:
        raise HTTPException(status_code=404, detail='Генерация не найдена или не принадлежит вам')
    
    await db.delete(generation)
    await db.commit()
    
    # Логируем удаление
    log = Log(
        user_id=current_user.id,
        action='delete_generation',
        item_id=str(generation_id),
        message=f"Удалена генерация ID: {generation_id}",
        status='completed'
    )
    db.add(log)
    await db.commit()
    
    return {"success": True, "message": "Генерация удалена"}


@router.get('/logs', response_model=list[LogResponse])
async def get_logs(
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """Получить последние 100 логов (только для админов)"""
    stmt = select(Log).order_by(desc(Log.timestamp)).limit(100)
    result = await db.execute(stmt)
    logs = result.scalars().all()
    return logs
