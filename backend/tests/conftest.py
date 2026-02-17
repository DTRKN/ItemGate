import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from main import app
from services.database import get_db
from models.base import Base


# Создание тестовой базы данных в памяти
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
)


@pytest_asyncio.fixture(scope="session")
async def test_db():
    """Создание тестовой базы данных"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield TestingSessionLocal

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(test_db):
    """Фикстура для сессии базы данных"""
    async with test_db() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture
async def client(db_session):
    """Фикстура для TestClient с тестовой БД"""

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user_data():
    """Тестовые данные пользователя"""
    return {
        "email": "test@example.com",
        "password": "testpass123",
        "full_name": "Test User"
    }


@pytest.fixture
def test_admin_data():
    """Тестовые данные админа"""
    return {
        "email": "admin@example.com",
        "password": "adminpass123",
        "full_name": "Admin User"
    }