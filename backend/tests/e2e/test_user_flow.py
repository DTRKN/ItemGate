import pytest
from fastapi.testclient import TestClient

from models.users import User, UserRole


class TestUserFlowE2E:
    """E2E тесты для полного потока работы с пользователями"""

    @pytest.mark.asyncio
    async def test_complete_user_registration_and_authentication_flow(self, client):
        """Тест полного потока: регистрация -> логин -> получение профиля -> выход"""

        # 1. Регистрация нового пользователя
        user_data = {
            "email": "e2e_test@example.com",
            "password": "securepass123",
            "full_name": "E2E Test User"
        }

        register_response = client.post("/auth/register", json=user_data)
        assert register_response.status_code == 201

        user_response = register_response.json()
        assert user_response["email"] == user_data["email"]
        assert user_response["full_name"] == user_data["full_name"]
        assert user_response["role"] == "user"
        assert user_response["is_active"] is True

        user_id = user_response["id"]

        # 2. Логин пользователя
        login_data = {
            "username": user_data["email"],
            "password": user_data["password"]
        }

        login_response = client.post("/auth/login", data=login_data)
        assert login_response.status_code == 200

        token_data = login_response.json()
        assert "access_token" in token_data
        assert token_data["token_type"] == "bearer"

        access_token = token_data["access_token"]

        # 3. Получение профиля пользователя
        headers = {"Authorization": f"Bearer {access_token}"}
        profile_response = client.get("/auth/me", headers=headers)
        assert profile_response.status_code == 200

        profile_data = profile_response.json()
        assert profile_data["id"] == user_id
        assert profile_data["email"] == user_data["email"]
        assert profile_data["full_name"] == user_data["full_name"]
        assert profile_data["role"] == "user"
        assert profile_data["is_active"] is True

        # 4. Проверка, что токен валиден для повторных запросов
        # (имитация повторного использования токена)
        profile_response_2 = client.get("/auth/me", headers=headers)
        assert profile_response_2.status_code == 200

    @pytest.mark.asyncio
    async def test_multiple_users_registration_and_isolation(self, client):
        """Тест регистрации нескольких пользователей и их изоляции"""

        # Регистрация первого пользователя
        user1_data = {
            "email": "user1@example.com",
            "password": "pass123",
            "full_name": "User One"
        }

        response1 = client.post("/auth/register", json=user1_data)
        assert response1.status_code == 201
        user1 = response1.json()

        # Регистрация второго пользователя
        user2_data = {
            "email": "user2@example.com",
            "password": "pass456",
            "full_name": "User Two"
        }

        response2 = client.post("/auth/register", json=user2_data)
        assert response2.status_code == 201
        user2 = response2.json()

        # Проверка, что пользователи разные
        assert user1["id"] != user2["id"]
        assert user1["email"] != user2["email"]

        # Логин первого пользователя
        login1_data = {"username": user1_data["email"], "password": user1_data["password"]}
        login1_response = client.post("/auth/login", data=login1_data)
        assert login1_response.status_code == 200
        token1 = login1_response.json()["access_token"]

        # Логин второго пользователя
        login2_data = {"username": user2_data["email"], "password": user2_data["password"]}
        login2_response = client.post("/auth/login", data=login2_data)
        assert login2_response.status_code == 200
        token2 = login2_response.json()["access_token"]

        # Проверка, что токены разные
        assert token1 != token2

        # Получение профиля первого пользователя
        headers1 = {"Authorization": f"Bearer {token1}"}
        profile1_response = client.get("/auth/me", headers=headers1)
        assert profile1_response.status_code == 200
        profile1 = profile1_response.json()
        assert profile1["email"] == user1_data["email"]

        # Получение профиля второго пользователя
        headers2 = {"Authorization": f"Bearer {token2}"}
        profile2_response = client.get("/auth/me", headers=headers2)
        assert profile2_response.status_code == 200
        profile2 = profile2_response.json()
        assert profile2["email"] == user2_data["email"]

        # Проверка изоляции: профиль первого != профилю второго
        assert profile1["id"] != profile2["id"]
        assert profile1["email"] != profile2["email"]

    @pytest.mark.asyncio
    async def test_user_inactive_scenario(self, client, db_session):
        """Тест сценария с неактивным пользователем"""

        # Создаем неактивного пользователя напрямую в БД
        from services.auth import get_password_hash
        from sqlalchemy import insert

        inactive_user_data = {
            "email": "inactive@example.com",
            "hashed_password": get_password_hash("password123"),
            "full_name": "Inactive User",
            "is_active": False,
            "role": UserRole.USER.value
        }

        # Вставляем в БД
        stmt = insert(User).values(**inactive_user_data)
        await db_session.execute(stmt)
        await db_session.commit()

        # Пытаемся войти
        login_data = {"username": "inactive@example.com", "password": "password123"}
        login_response = client.post("/auth/login", data=login_data)

        # Должен быть успех логина (проверка пароля проходит)
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]

        # Но при попытке получить профиль - ошибка
        headers = {"Authorization": f"Bearer {token}"}
        profile_response = client.get("/auth/me", headers=headers)

        assert profile_response.status_code == 400
        assert "Inactive user" in profile_response.json()["detail"]

    @pytest.mark.asyncio
    async def test_admin_user_flow(self, client, db_session):
        """Тест потока для админа"""

        # Создаем админа напрямую в БД
        from services.auth import get_password_hash
        from sqlalchemy import insert

        admin_data = {
            "email": "admin@example.com",
            "hashed_password": get_password_hash("adminpass"),
            "full_name": "Admin User",
            "is_active": True,
            "role": UserRole.ADMIN.value
        }

        stmt = insert(User).values(**admin_data)
        await db_session.execute(stmt)
        await db_session.commit()

        # Логин админа
        login_data = {"username": "admin@example.com", "password": "adminpass"}
        login_response = client.post("/auth/login", data=login_data)
        assert login_response.status_code == 200

        token = login_response.json()["access_token"]

        # Получение профиля админа
        headers = {"Authorization": f"Bearer {token}"}
        profile_response = client.get("/auth/me", headers=headers)
        assert profile_response.status_code == 200

        profile = profile_response.json()
        assert profile["role"] == "admin"
        assert profile["email"] == "admin@example.com"