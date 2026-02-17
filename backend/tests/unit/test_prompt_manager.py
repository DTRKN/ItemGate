import pytest
import yaml
from unittest.mock import patch, mock_open
from pathlib import Path
from services.prompt_manager import PromptManager, prompt_manager


class TestPromptManager:
    """Тесты для менеджера промптов"""

    def test_prompt_manager_instance(self):
        """Тест создания экземпляра PromptManager"""
        manager = PromptManager()
        assert isinstance(manager, PromptManager)

    def test_global_prompt_manager_instance(self):
        """Тест глобального экземпляра prompt_manager"""
        assert isinstance(prompt_manager, PromptManager)

    @pytest.mark.asyncio
    async def test_load_system_prompt_success(self):
        """Тест успешной загрузки системного промпта"""
        mock_yaml_data = {"system": "Test system prompt content"}
        mock_yaml_content = yaml.dump(mock_yaml_data)

        with patch("builtins.open", mock_open(read_data=mock_yaml_content)):
            result = await PromptManager.load_system_prompt("test/path.yaml")

            assert result == "Test system prompt content"

    @pytest.mark.asyncio
    async def test_load_system_prompt_file_not_found(self):
        """Тест обработки ошибки FileNotFoundError"""
        with patch("builtins.open", side_effect=FileNotFoundError("File not found")):
            with pytest.raises(FileNotFoundError):
                await PromptManager.load_system_prompt("nonexistent/path.yaml")

    @pytest.mark.asyncio
    async def test_load_system_prompt_invalid_yaml(self):
        """Тест обработки ошибки невалидного YAML"""
        invalid_yaml = "invalid: yaml: content: [unclosed"

        with patch("builtins.open", mock_open(read_data=invalid_yaml)):
            with pytest.raises(yaml.YAMLError):
                await PromptManager.load_system_prompt("test/path.yaml")

    @pytest.mark.asyncio
    async def test_load_system_prompt_missing_system_key(self):
        """Тест обработки YAML без ключа 'system'"""
        mock_yaml_data = {"other_key": "some value"}
        mock_yaml_content = yaml.dump(mock_yaml_data)

        with patch("builtins.open", mock_open(read_data=mock_yaml_content)):
            with pytest.raises(KeyError):
                await PromptManager.load_system_prompt("test/path.yaml")

    @pytest.mark.asyncio
    async def test_load_system_prompt_path_conversion(self):
        """Тест конвертации пути в Path объект"""
        mock_yaml_data = {"system": "Test content"}
        mock_yaml_content = yaml.dump(mock_yaml_data)

        with patch("builtins.open", mock_open(read_data=mock_yaml_content)) as mock_file:
            await PromptManager.load_system_prompt("test/path.yaml")

            # Проверяем, что путь был конвертирован в Path
            args, kwargs = mock_file.call_args
            assert isinstance(args[0], Path)
            assert args[0] == Path("test/path.yaml")