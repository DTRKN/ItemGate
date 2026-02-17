import pytest
from fastapi.testclient import TestClient
from fastapi.middleware.cors import CORSMiddleware
from main import app


class TestMainApp:
    """Тесты для основного приложения"""

    def test_app_creation(self):
        """Тест создания FastAPI приложения"""
        assert app.title == "ItemGate API"
        assert app.version == "0.1.0"

    def test_health_endpoints(self):
        """Тест health check endpoints"""
        client = TestClient(app)

        # Тест корневого health check
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["service"] == "ItemGate API"

        # Тест /health endpoint
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    def test_cors_middleware(self):
        """Тест CORS middleware"""
        # Проверяем, что CORS middleware добавлен
        assert any(m.cls is CORSMiddleware for m in app.user_middleware)

    def test_router_inclusion(self):
        """Тест включения роутеров"""
        # Проверяем, что auth роутер включен
        auth_route = None
        for route in app.routes:
            if hasattr(route, 'path') and '/auth' in str(route.path):
                auth_route = route
                break

        assert auth_route is not None