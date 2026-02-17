"""
Скрипт для создания первого администратора

Запуск: python create_admin.py
"""
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import ProgrammingError
from services.auth import get_password_hash
from models.users import User, UserRole
from config import Config
from schemas.user import UserCreate
from pydantic import ValidationError

async def create_admin():
    """Создание первого администратора"""
    config = Config()
    
    # Создаем engine
    engine = create_async_engine(config.database_url, echo=True)
    
    # Создаем sessionmaker
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as session:
        # Проверяем, есть ли уже админ
        from sqlalchemy import select
        try:
            result = await session.execute(
                select(User).where(User.role == UserRole.ADMIN)
            )
        except ProgrammingError as e:
            error_text = str(e)
            if "UndefinedTableError" in error_text or 'relation "users" does not exist' in error_text:
                print("❌ Таблица users не найдена. Сначала примени миграции.")
                print("   Команда: docker compose exec backend alembic upgrade head")
                return
            raise
        existing_admin = result.scalar_one_or_none()

        # await session.delete(existing_admin)
        # await session.commit()
        
        if existing_admin:
            print(f"❌ Администратор уже существует: {existing_admin.email}")
            return
        
        # Создаем нового админа
        admin_email = input("Email администратора: ").strip()
        admin_password = input("Пароль администратора: ").strip()
        admin_name = input("Имя администратора (опционально): ").strip() or None

        # Валидация через Pydantic (EmailStr, минимальная длина пароля и т.д.)
        try:
            UserCreate(email=admin_email, password=admin_password, full_name=admin_name)
        except ValidationError as e:
            print("❌ Ошибка валидации данных:")
            for err in e.errors():
                loc = ".".join([str(l) for l in err.get('loc', [])])
                msg = err.get('msg')
                print(f" - {loc}: {msg}")
            return
        
        admin = User(
            email=admin_email,
            hashed_password=get_password_hash(admin_password),
            full_name=admin_name,
            role=UserRole.ADMIN,
            is_active=True
        )
        
        session.add(admin)
        await session.commit()
        await session.refresh(admin)
        
        print(f"\n✅ Администратор создан:")
        print(f"   Email: {admin.email}")
        print(f"   Роль: {admin.role.value}")
        print(f"   ID: {admin.id}")
    
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(create_admin())
