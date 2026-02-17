import pytest
import json
from unittest.mock import patch, AsyncMock, MagicMock
from fastapi import HTTPException
from pydantic import ValidationError
import httpx

from services.ai_client import OpenRouterClient, openRouterClient
from schemas.item import ItemInfo_ai


class TestOpenRouterClient:
    """Тесты для OpenRouter AI клиента"""

    def test_client_initialization(self):
        """Тест инициализации клиента"""
        api_key = "test_key"
        client = OpenRouterClient(api_key)

        assert client.api_key == api_key
        assert client.base_url == "https://openrouter.ai"
        assert isinstance(client.client, httpx.AsyncClient)

    def test_global_client_instance(self):
        """Тест глобального экземпляра клиента"""
        # Проверяем, что экземпляр создан (даже если API_KEY None)
        assert isinstance(openRouterClient, OpenRouterClient)

    @pytest.mark.asyncio
    async def test_get_response_success(self):
        """Тест успешного получения ответа от AI"""
        # Мокаем зависимости
        mock_system_prompt = {"content": "Test system prompt"}

        mock_response_data = {
            "Description": "Test SEO description",
            "Words": ["test", "keywords"]
        }

        mock_api_response = {
            "choices": [{
                "message": {
                    "content": json.dumps(mock_response_data)
                }
            }]
        }

        client = OpenRouterClient("test_key")

        with patch.object(client.client, 'post') as mock_post, \
             patch('services.prompt_manager.prompt_manager.load_system_prompt', return_value=mock_system_prompt):

            mock_response = MagicMock()
            mock_response.json.return_value = mock_api_response
            mock_response.raise_for_status.return_value = None
            mock_post.return_value = mock_response

            result = await client.get_response("test user data")

            assert isinstance(result, ItemInfo_ai)
            assert result.Description == "Test SEO description"
            assert result.Words == ["test", "keywords"]

    @pytest.mark.asyncio
    async def test_get_response_http_error(self):
        """Тест обработки HTTP ошибки"""
        client = OpenRouterClient("test_key")

        with patch.object(client.client, 'post') as mock_post, \
             patch('services.prompt_manager.prompt_manager.load_system_prompt'):

            mock_response = MagicMock()
            mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
                "Bad Request", request=MagicMock(), response=MagicMock()
            )
            mock_post.return_value = mock_response

            with pytest.raises(httpx.HTTPStatusError):
                await client.get_response("test data")

    @pytest.mark.asyncio
    async def test_get_response_invalid_json(self):
        """Тест обработки невалидного JSON от AI"""
        mock_api_response = {
            "choices": [{
                "message": {
                    "content": "invalid json content"
                }
            }]
        }

        client = OpenRouterClient("test_key")

        with patch.object(client.client, 'post') as mock_post, \
             patch('services.prompt_manager.prompt_manager.load_system_prompt'):

            mock_response = MagicMock()
            mock_response.json.return_value = mock_api_response
            mock_response.raise_for_status.return_value = None
            mock_post.return_value = mock_response

            with pytest.raises(json.JSONDecodeError):
                await client.get_response("test data")

    @pytest.mark.asyncio
    async def test_get_response_validation_error(self):
        """Тест обработки ошибки валидации Pydantic"""
        # Создаем невалидные данные (отсутствует обязательное поле)
        mock_response_data = {
            "seo_description": "Test description",
            "seo_keywords": ["test"]
            # отсутствует seo_title
        }

        mock_api_response = {
            "choices": [{
                "message": {
                    "content": json.dumps(mock_response_data)
                }
            }]
        }

        client = OpenRouterClient("test_key")

        with patch.object(client.client, 'post') as mock_post, \
             patch('services.prompt_manager.prompt_manager.load_system_prompt'):

            mock_response = MagicMock()
            mock_response.json.return_value = mock_api_response
            mock_response.raise_for_status.return_value = None
            mock_post.return_value = mock_response

            with pytest.raises(HTTPException) as exc_info:
                await client.get_response("test data")

            assert exc_info.value.status_code == 502
            assert "unexpected schema" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_get_response_prompt_loading_error(self):
        """Тест обработки ошибки загрузки промпта"""
        client = OpenRouterClient("test_key")

        with patch('services.prompt_manager.prompt_manager.load_system_prompt', side_effect=FileNotFoundError):
            with pytest.raises(FileNotFoundError):
                await client.get_response("test data")