import pytest
from models.users import User, UserRole


class TestUserModel:
    """Тесты для модели User"""

    def test_user_creation(self):
        """Тест создания пользователя"""
        user = User(
            email="test@example.com",
            hashed_password="hashed_password",
            full_name="Test User",
            role=UserRole.USER,
            is_active=True
        )

        assert user.email == "test@example.com"
        assert user.hashed_password == "hashed_password"
        assert user.full_name == "Test User"
        assert user.role == UserRole.USER
        assert user.is_active is True

    def test_user_repr(self):
        """Тест строкового представления пользователя"""
        user = User(
            email="test@example.com",
            hashed_password="hashed_password",
            role=UserRole.USER
        )

        expected_repr = f"<User(email={user.email}, role={user.role})>"
        assert repr(user) == expected_repr

    def test_user_role_enum(self):
        """Тест перечисления ролей пользователей"""
        assert UserRole.USER.value == "user"
        assert UserRole.ADMIN.value == "admin"

        # Проверка, что роли уникальны
        assert UserRole.USER != UserRole.ADMIN

    def test_user_default_values(self):
        """Тест значений по умолчанию"""
        user = User(
            email="test@example.com",
            hashed_password="hashed_password"
        )

        # SQLAlchemy Column default применяется на этапе INSERT в БД,
        # поэтому до flush/commit значения могут быть None.
        assert user.role is None
        assert user.is_active is None
        assert user.full_name is None