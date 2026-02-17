import pytest
from unittest.mock import patch
from config import Config, config


class TestConfig:
    """Тесты для конфигурации приложения"""

    def test_config_defaults(self):
        """Тест значений по умолчанию"""
        with patch.object(Config, "DB_NAME", "itemgate"), \
             patch.object(Config, "DB_USER", "postgres"), \
             patch.object(Config, "DB_PASSWORD", "postgres"), \
             patch.object(Config, "DB_HOST", "localhost"), \
             patch.object(Config, "DB_PORT", "5432"), \
             patch.object(Config, "AI_KEY", None), \
             patch.object(Config, "USE_POSTGRES", False):
            cfg = Config()

            assert cfg.DB_NAME == "itemgate"
            assert cfg.DB_USER == "postgres"
            assert cfg.DB_PASSWORD == "postgres"
            assert cfg.DB_HOST == "localhost"
            assert cfg.DB_PORT == "5432"
            assert cfg.AI_KEY is None
            assert cfg.USE_POSTGRES is False
            assert cfg.prompt_system_generate_info == "prompts/info_for_seller.yaml"

    def test_config_with_env_vars(self):
        """Тест конфигурации с переменными окружения"""
        with patch.object(Config, "DB_NAME", "test_db"), \
             patch.object(Config, "DB_USER", "test_user"), \
             patch.object(Config, "DB_PASSWORD", "test_pass"), \
             patch.object(Config, "DB_HOST", "test_host"), \
             patch.object(Config, "DB_PORT", "9999"), \
             patch.object(Config, "AI_KEY", "test_ai_key"), \
             patch.object(Config, "USE_POSTGRES", True):
            cfg = Config()

            assert cfg.DB_NAME == "test_db"
            assert cfg.DB_USER == "test_user"
            assert cfg.DB_PASSWORD == "test_pass"
            assert cfg.DB_HOST == "test_host"
            assert cfg.DB_PORT == "9999"
            assert cfg.AI_KEY == "test_ai_key"
            assert cfg.USE_POSTGRES is True

    def test_database_url_sqlite(self):
        """Тест URL базы данных для SQLite"""
        with patch.object(Config, "USE_POSTGRES", False), \
             patch.object(Config, "DB_NAME", "itemgate"):
            cfg = Config()

            expected_url = "sqlite+aiosqlite:///./itemgate_database.db"
            assert cfg.database_url == expected_url

    def test_database_url_postgres(self):
        """Тест URL базы данных для PostgreSQL"""
        with patch.object(Config, "USE_POSTGRES", True), \
             patch.object(Config, "DB_USER", "testuser"), \
             patch.object(Config, "DB_PASSWORD", "testpass"), \
             patch.object(Config, "DB_HOST", "testhost"), \
             patch.object(Config, "DB_PORT", "5432"), \
             patch.object(Config, "DB_NAME", "testdb"):
            cfg = Config()

            expected_url = "postgresql+asyncpg://testuser:testpass@testhost:5432/testdb"
            assert cfg.database_url == expected_url

    def test_use_postgres_case_insensitive(self):
        """Тест логического включения PostgreSQL"""
        with patch.object(Config, "USE_POSTGRES", True):
            cfg = Config()
            assert cfg.USE_POSTGRES is True

    def test_global_config_instance(self):
        """Тест глобального экземпляра конфигурации"""
        assert isinstance(config, Config)
        assert hasattr(config, 'database_url')