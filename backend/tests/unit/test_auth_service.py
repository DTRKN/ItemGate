import pytest
from unittest.mock import patch, MagicMock
from datetime import timedelta
from jose import jwt

from services.auth import (
    verify_password,
    get_password_hash,
    create_access_token,
    authenticate_user,
    get_current_user,
    get_current_active_user,
    get_current_admin_user,
    SECRET_KEY,
    ALGORITHM
)
from models.users import User, UserRole


class TestPasswordFunctions:
    """Тесты функций работы с паролями"""

    def test_get_password_hash(self):
        """Тест хеширования пароля"""
        password = "testpassword"
        hashed = get_password_hash(password)

        assert hashed != password
        assert isinstance(hashed, str)
        assert len(hashed) > 0

    def test_verify_password_correct(self):
        """Тест проверки правильного пароля"""
        password = "testpassword"
        hashed = get_password_hash(password)

        assert verify_password(password, hashed) is True

    def test_verify_password_incorrect(self):
        """Тест проверки неправильного пароля"""
        password = "testpassword"
        wrong_password = "wrongpassword"
        hashed = get_password_hash(password)

        assert verify_password(wrong_password, hashed) is False


class TestTokenFunctions:
    """Тесты функций работы с токенами"""

    def test_create_access_token(self):
        """Тест создания токена"""
        data = {"sub": "test@example.com", "role": "user"}
        expires_delta = timedelta(minutes=30)

        token = create_access_token(data, expires_delta)

        assert isinstance(token, str)
        assert len(token) > 0

        # Декодируем токен для проверки
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert payload["sub"] == "test@example.com"
        assert payload["role"] == "user"
        assert "exp" in payload

    def test_create_access_token_no_expires(self):
        """Тест создания токена без expires_delta"""
        data = {"sub": "test@example.com"}

        token = create_access_token(data)

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert payload["sub"] == "test@example.com"
        assert "exp" in payload


class TestAuthenticationFunctions:
    """Тесты функций аутентификации"""

    @pytest.mark.asyncio
    async def test_authenticate_user_success(self):
        """Тест успешной аутентификации"""
        # Мокаем базу данных
        mock_db = MagicMock()
        mock_user = User(
            id=1,
            email="test@example.com",
            hashed_password=get_password_hash("password"),
            full_name="Test User",
            is_active=True,
            role=UserRole.USER
        )

        with patch('services.auth.get_user_by_email', return_value=mock_user):
            result = await authenticate_user(mock_db, "test@example.com", "password")

            assert result == mock_user

    @pytest.mark.asyncio
    async def test_authenticate_user_wrong_password(self):
        """Тест аутентификации с неправильным паролем"""
        mock_db = MagicMock()
        mock_user = User(
            id=1,
            email="test@example.com",
            hashed_password=get_password_hash("password"),
            full_name="Test User",
            is_active=True,
            role=UserRole.USER
        )

        with patch('services.auth.get_user_by_email', return_value=mock_user):
            result = await authenticate_user(mock_db, "test@example.com", "wrongpassword")

            assert result is None

    @pytest.mark.asyncio
    async def test_authenticate_user_user_not_found(self):
        """Тест аутентификации с несуществующим пользователем"""
        mock_db = MagicMock()

        with patch('services.auth.get_user_by_email', return_value=None):
            result = await authenticate_user(mock_db, "nonexistent@example.com", "password")

            assert result is None


class TestUserValidationFunctions:
    """Тесты функций валидации пользователей"""

    @pytest.mark.asyncio
    async def test_get_current_active_user_active(self):
        """Тест получения активного пользователя"""
        user = User(
            id=1,
            email="test@example.com",
            hashed_password="hashed",
            full_name="Test User",
            is_active=True,
            role=UserRole.USER
        )

        result = await get_current_active_user(user)
        assert result == user

    @pytest.mark.asyncio
    async def test_get_current_active_user_inactive(self):
        """Тест получения неактивного пользователя"""
        user = User(
            id=1,
            email="test@example.com",
            hashed_password="hashed",
            full_name="Test User",
            is_active=False,
            role=UserRole.USER
        )

        with pytest.raises(Exception) as exc_info:
            await get_current_active_user(user)

        assert "Inactive user" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_current_admin_user_admin(self):
        """Тест получения админа"""
        user = User(
            id=1,
            email="admin@example.com",
            hashed_password="hashed",
            full_name="Admin User",
            is_active=True,
            role=UserRole.ADMIN
        )

        result = await get_current_admin_user(user)
        assert result == user

    @pytest.mark.asyncio
    async def test_get_current_admin_user_not_admin(self):
        """Тест получения не-админа"""
        user = User(
            id=1,
            email="user@example.com",
            hashed_password="hashed",
            full_name="Regular User",
            is_active=True,
            role=UserRole.USER
        )

        with pytest.raises(Exception) as exc_info:
            await get_current_admin_user(user)

        assert "Not enough permissions" in str(exc_info.value)