import pytest
from pydantic import ValidationError
from schemas.user import (
    UserBase, UserCreate, UserLogin, UserResponse,
    Token, TokenData, UserRole
)


class TestUserSchemas:
    """Тесты для схем пользователя"""

    def test_user_base_schema(self):
        """Тест базовой схемы пользователя"""
        user_data = {
            "email": "test@example.com",
            "full_name": "Test User"
        }

        user = UserBase(**user_data)
        assert user.email == "test@example.com"
        assert user.full_name == "Test User"

    def test_user_base_schema_optional_full_name(self):
        """Тест базовой схемы с опциональным full_name"""
        user_data = {
            "email": "test@example.com"
        }

        user = UserBase(**user_data)
        assert user.email == "test@example.com"
        assert user.full_name is None

    def test_user_create_schema(self):
        """Тест схемы создания пользователя"""
        user_data = {
            "email": "test@example.com",
            "password": "securepass123",
            "full_name": "Test User"
        }

        user = UserCreate(**user_data)
        assert user.email == "test@example.com"
        assert user.password == "securepass123"
        assert user.full_name == "Test User"

    def test_user_create_password_validation(self):
        """Тест валидации пароля при создании"""
        # Слишком короткий пароль
        with pytest.raises(ValidationError):
            UserCreate(
                email="test@example.com",
                password="123"  # Менее 6 символов
            )

        # Валидный пароль
        user = UserCreate(
            email="test@example.com",
            password="validpass"
        )
        assert user.password == "validpass"

    def test_user_login_schema(self):
        """Тест схемы логина"""
        login_data = {
            "email": "test@example.com",
            "password": "password123"
        }

        login = UserLogin(**login_data)
        assert login.email == "test@example.com"
        assert login.password == "password123"

    def test_user_response_schema(self):
        """Тест схемы ответа пользователя"""
        from datetime import datetime

        response_data = {
            "id": 1,
            "email": "test@example.com",
            "full_name": "Test User",
            "role": "user",
            "is_active": True,
            "created_at": datetime.now()
        }

        response = UserResponse(**response_data)
        assert response.id == 1
        assert response.email == "test@example.com"
        assert response.full_name == "Test User"
        assert response.role == "user"
        assert response.is_active is True

    def test_token_schema(self):
        """Тест схемы токена"""
        token_data = {
            "access_token": "jwt.token.here",
            "token_type": "bearer"
        }

        token = Token(**token_data)
        assert token.access_token == "jwt.token.here"
        assert token.token_type == "bearer"

    def test_token_default_type(self):
        """Тест значения по умолчанию для token_type"""
        token = Token(access_token="jwt.token.here")
        assert token.token_type == "bearer"

    def test_token_data_schema(self):
        """Тест схемы данных токена"""
        token_data = {
            "email": "test@example.com",
            "role": "user"
        }

        data = TokenData(**token_data)
        assert data.email == "test@example.com"
        assert data.role == "user"

    def test_token_data_optional_fields(self):
        """Тест опциональных полей в TokenData"""
        # Все поля опциональны
        data = TokenData()
        assert data.email is None
        assert data.role is None

        # Частично заполненные
        data = TokenData(email="test@example.com")
        assert data.email == "test@example.com"
        assert data.role is None

    def test_email_validation(self):
        """Тест валидации email"""
        # Валидный email
        user = UserBase(email="valid@example.com")
        assert user.email == "valid@example.com"

        # Невалидный email
        with pytest.raises(ValidationError):
            UserBase(email="invalid-email")