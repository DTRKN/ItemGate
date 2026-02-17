import pytest
from unittest.mock import patch, AsyncMock
from services.database import get_db


class TestDatabaseService:
    """Тесты для сервиса базы данных"""

    @pytest.mark.asyncio
    async def test_get_db_success_commit_and_close(self):
        """При успешном использовании get_db вызываются commit и close"""
        mock_session = AsyncMock()
        mock_session.commit = AsyncMock()
        mock_session.rollback = AsyncMock()
        mock_session.close = AsyncMock()

        mock_cm = AsyncMock()
        mock_cm.__aenter__.return_value = mock_session
        mock_cm.__aexit__.return_value = None

        with patch("services.database.AsyncSessionLocal", return_value=mock_cm):
            gen = get_db()
            session = await anext(gen)
            assert session is mock_session

            with pytest.raises(StopAsyncIteration):
                await anext(gen)

            mock_session.commit.assert_awaited_once()
            mock_session.rollback.assert_not_called()
            mock_session.close.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_get_db_error_rollback_and_close(self):
        """При ошибке внутри get_db вызываются rollback и close"""
        mock_session = AsyncMock()
        mock_session.commit = AsyncMock()
        mock_session.rollback = AsyncMock()
        mock_session.close = AsyncMock()

        mock_cm = AsyncMock()
        mock_cm.__aenter__.return_value = mock_session
        mock_cm.__aexit__.return_value = None

        with patch("services.database.AsyncSessionLocal", return_value=mock_cm):
            gen = get_db()
            await anext(gen)

            with pytest.raises(RuntimeError):
                await gen.athrow(RuntimeError("db failure"))

            mock_session.commit.assert_not_called()
            mock_session.rollback.assert_awaited_once()
            mock_session.close.assert_awaited_once()