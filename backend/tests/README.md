# Тестирование ItemGate API

Этот документ описывает архитектуру и запуск тестов для ItemGate API.

## Архитектура тестирования

### Уровни тестирования

1. **Unit tests** (`tests/unit/`)
   - Тестирование отдельных функций и методов
   - Минимальные зависимости, использование моков
   - Быстрое выполнение

2. **Integration tests** (`tests/integration/`)
   - Тестирование взаимодействия между компонентами
   - Использование тестовой базы данных
   - Тестирование API endpoints

3. **E2E tests** (`tests/e2e/`)
   - Тестирование полного пользовательского сценария
   - От регистрации до использования функционала
   - Максимальная реалистичность

### Структура тестов

```
tests/
├── conftest.py          # Общие фикстуры и конфигурация
├── unit/               # Unit тесты
│   └── test_auth_service.py
├── integration/        # Integration тесты
│   └── test_auth_api.py
└── e2e/               # E2E тесты
    └── test_user_flow.py
```

## Запуск тестов

### Все тесты
```bash
python run_tests.py
```

### Только unit тесты
```bash
python run_tests.py unit
```

### Только integration тесты
```bash
python run_tests.py integration
```

### Только E2E тесты
```bash
python run_tests.py e2e
```

### Конкретный файл
```bash
python run_tests.py tests/unit/test_auth_service.py
```

## Отчет о покрытии

После запуска тестов генерируется отчет о покрытии кода:
- Консольный отчет с процентами покрытия
- HTML отчет в папке `htmlcov/`

Минимальный порог покрытия: 80%

## Фикстуры

### Основные фикстуры (conftest.py)

- `test_db`: Тестовая база данных в памяти
- `db_session`: Сессия базы данных для тестов
- `client`: TestClient FastAPI с тестовой БД
- `test_user_data`: Тестовые данные пользователя
- `test_admin_data`: Тестовые данные админа

## Примеры тестов

### Unit тест
```python
def test_get_password_hash():
    password = "testpassword"
    hashed = get_password_hash(password)
    assert hashed != password
    assert verify_password(password, hashed) is True
```

### Integration тест
```python
def test_register_user_success(self, client, test_user_data):
    response = client.post("/auth/register", json=test_user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == test_user_data["email"]
```

### E2E тест
```python
def test_complete_user_registration_and_authentication_flow(self, client):
    # Регистрация -> Логин -> Получение профиля
    # Полный сценарий использования
```

## Лучшие практики

1. **Изоляция**: Каждый тест независим, использует свежую БД
2. **Читаемость**: Описательные имена тестов
3. **Покрытие**: Тестировать happy path и edge cases
4. **Быстродействие**: Unit тесты должны быть быстрыми
5. **Моки**: Использовать моки для внешних зависимостей

## Добавление новых тестов

1. Определить уровень тестирования
2. Создать файл в соответствующей папке
3. Использовать существующие фикстуры
4. Следовать паттернам именования
5. Добавить документацию

## CI/CD готовность

Хотя CI/CD не планируется, тесты готовы для интеграции:
- pytest с маркерами для разных типов тестов
- Отчеты о покрытии
- Возможность запуска в контейнерах
- Конфигурация через pytest.ini