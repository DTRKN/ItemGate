import pytest
from unittest.mock import patch, MagicMock
from services.logger import log_info, log_error, log_warning


class TestLogger:
    """Тесты для сервиса логирования"""

    @patch('services.logger.logger')
    def test_log_info(self, mock_logger):
        """Тест логирования информационных сообщений"""
        message = "Test info message"
        log_info(message)

        mock_logger.info.assert_called_once_with(message)

    @patch('services.logger.logger')
    def test_log_error_with_exception(self, mock_logger):
        """Тест логирования ошибок с исключением"""
        message = "Test error message"
        exception = ValueError("Test exception")

        log_error(message, exc_info=exception)

        mock_logger.error.assert_called_once_with(message, exc_info=exception)

    @patch('services.logger.logger')
    def test_log_error_without_exception(self, mock_logger):
        """Тест логирования ошибок без исключения"""
        message = "Test error message"

        log_error(message)

        mock_logger.error.assert_called_once_with(message, exc_info=None)

    @patch('services.logger.logger')
    def test_log_warning(self, mock_logger):
        """Тест логирования предупреждений"""
        message = "Test warning message"
        log_warning(message)

        mock_logger.warning.assert_called_once_with(message)