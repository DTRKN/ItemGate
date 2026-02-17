import pytest
from fastapi import HTTPException
from sqlalchemy import select

from models.users import User, UserRole


class TestAuthAPI:
    """Интеграционные тесты для API аутентификации"""

    @pytest.mark.asyncio
    async def test_register_user_success(self, client, test_user_data):
        """Тест успешной регистрации пользователя"""
        response = client.post("/auth/register", json=test_user_data)

        assert response.status_code == 201
        data = response.json()

        assert data["email"] == test_user_data["email"]
        assert data["full_name"] == test_user_data["full_name"]
        assert data["role"] == "user"
        assert data["is_active"] is True
        assert "id" in data
        assert "created_at" in data

    @pytest.mark.asyncio
    async def test_register_user_duplicate_email(self, client, test_user_data):
        """Тест регистрации с существующим email"""
        # Сначала регистрируем пользователя
        client.post("/auth/register", json=test_user_data)

        # Пытаемся зарегистрировать снова
        response = client.post("/auth/register", json=test_user_data)

        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_register_user_invalid_email(self, client):
        """Тест регистрации с невалидным email"""
        invalid_data = {
            "email": "invalid-email",
            "password": "testpass123",
            "full_name": "Test User"
        }

        response = client.post("/auth/register", json=invalid_data)

        assert response.status_code == 422  # Validation error

    @pytest.mark.asyncio
    async def test_register_user_short_password(self, client):
        """Тест регистрации с коротким паролем"""
        invalid_data = {
            "email": "test@example.com",
            "password": "123",  # Слишком короткий
            "full_name": "Test User"
        }

        response = client.post("/auth/register", json=invalid_data)

        assert response.status_code == 422  # Validation error

    @pytest.mark.asyncio
    async def test_login_success(self, client, test_user_data):
        """Тест успешного логина"""
        # Сначала регистрируем пользователя
        client.post("/auth/register", json=test_user_data)

        # Логинимся
        login_data = {
            "username": test_user_data["email"],  # OAuth2 использует username
            "password": test_user_data["password"]
        }

        response = client.post("/auth/login", data=login_data)

        assert response.status_code == 200
        data = response.json()

        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert isinstance(data["access_token"], str)

    @pytest.mark.asyncio
    async def test_login_json_success(self, client, test_user_data):
        """Тест успешного логина через JSON"""
        # Сначала регистрируем пользователя
        client.post("/auth/register", json=test_user_data)

        # Логинимся через JSON
        login_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"]
        }

        response = client.post("/auth/login-json", json=login_data)

        assert response.status_code == 200
        data = response.json()

        assert "access_token" in data
        assert data["token_type"] == "bearer"

    @pytest.mark.asyncio
    async def test_login_wrong_password(self, client, test_user_data):
        """Тест логина с неправильным паролем"""
        # Сначала регистрируем пользователя
        client.post("/auth/register", json=test_user_data)

        # Пытаемся войти с неправильным паролем
        login_data = {
            "username": test_user_data["email"],
            "password": "wrongpassword"
        }

        response = client.post("/auth/login", data=login_data)

        assert response.status_code == 401
        assert "Incorrect email or password" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_login_nonexistent_user(self, client):
        """Тест логина несуществующего пользователя"""
        login_data = {
            "username": "nonexistent@example.com",
            "password": "password"
        }

        response = client.post("/auth/login", data=login_data)

        assert response.status_code == 401
        assert "Incorrect email or password" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_get_me_authenticated(self, client, test_user_data):
        """Тест получения профиля авторизованного пользователя"""
        # Регистрируем и логинимся
        client.post("/auth/register", json=test_user_data)

        login_data = {
            "username": test_user_data["email"],
            "password": test_user_data["password"]
        }
        login_response = client.post("/auth/login", data=login_data)
        token = login_response.json()["access_token"]

        # Получаем профиль
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/auth/me", headers=headers)

        assert response.status_code == 200
        data = response.json()

        assert data["email"] == test_user_data["email"]
        assert data["full_name"] == test_user_data["full_name"]
        assert data["role"] == "user"
        assert data["is_active"] is True

    @pytest.mark.asyncio
    async def test_get_me_unauthenticated(self, client):
        """Тест получения профиля без авторизации"""
        response = client.get("/auth/me")

        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_get_me_invalid_token(self, client):
        """Тест получения профиля с невалидным токеном"""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/auth/me", headers=headers)

        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_health_check(self, client):
        """Тест health check endpoint"""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()

        assert data["status"] == "ok"
        assert data["service"] == "ItemGate API"

    @pytest.mark.asyncio
    async def test_health_endpoint(self, client):
        """Тест /health endpoint"""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()

        assert data["status"] == "healthy"