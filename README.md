![MVP Alpha](https://img.shields.io/badge/MVP-alpha-ff8c00)
# ItemGate — AI-платформа для продавцов маркетплейсов

![Смотреть демо](./ItemGateVid.mp4)

<video src="./ItemGateVid.mp4" width="320" height="240" controls></video>

ItemGate помогает продавцам быстро создавать SEO-оптимизированные карточки товаров: от загрузки каталога до генерации описаний и ключевых слов с помощью ИИ.  
Фокус проекта — MVP, скорость запуска и практическая польза для реальной e-commerce работы.

![AI](https://img.shields.io/badge/AI-OpenAI%20Compatible-412991?logo=openai&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.128-009688?logo=fastapi&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-v2-E92063)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00?logo=sqlalchemy&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-4169E1?logo=postgresql&logoColor=white)
![Alembic](https://img.shields.io/badge/Alembic-Migrations-333333)
![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=111)
![Vite](https://img.shields.io/badge/Vite-7-646CFF?logo=vite&logoColor=white)
![Vitest](https://img.shields.io/badge/Vitest-Frontend%20Tests-6E9F18)
![Pytest](https://img.shields.io/badge/Pytest-Backend%20Tests-0A9EDC?logo=pytest&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)

## Что это за проект

ItemGate — это веб-сервис, который автоматизирует создание контента для карточек товаров:
- загружает товары из API Sima-Land;
- хранит каталог в базе данных;
- генерирует SEO-описание и ключевые слова через ИИ;
- сохраняет историю генераций;
- позволяет быстро редактировать результат в интерфейсе;
- экспортирует данные в Excel.

## Быстрый запуск (Docker)

1. Перейди в папку backend:

`cd src/backend`

2. Подними проект:

`docker compose up -d --build`

При старте автоматически выполняется сервис `migrate` (`alembic upgrade head`), поэтому таблицы создаются до запуска backend.

3. Открой сервисы:
- Frontend: `http://localhost`
- Backend API: `http://localhost:8000`
- Health-check: `http://localhost:8000/health`

## Создание администратора

После запуска создай первого администратора:

`docker compose exec backend python create_admin.py`

Далее введи `email`, `password` и (опционально) имя.

## Загрузка товаров из Sima-Land

Загрузка выполняется на сайте, во вкладке **«Загрузка»** (доступ только для admin).

Backend endpoint, который вызывает интерфейс:

`GET /sima-land/loading_words_db/{count}`

Пример: загрузка 500 товаров:

`http://localhost:8000/sima-land/loading_words_db/500`

## Если что-то работает некорректно — запусти тесты

### Backend тесты

Локально:

`cd src/backend && python quick_test.py`

Или через Docker profile:

`docker compose --profile test up --build tests`

Если запускаешь из корня проекта, используй:

`docker compose -f src/backend/docker-compose.yml up -d --build`

### Frontend тесты

`cd src/frontend && npm run test:run`

## Основные разделы проекта

- **Authentication**: регистрация, логин, роли пользователей (user/admin)
- **Catalog (Sima-Land)**: загрузка и хранение общего каталога товаров
- **AI Generation**: генерация SEO-описаний и ключевых слов
- **Item Management**: просмотр и ручное редактирование данных
- **Excel Export**: выгрузка истории и результатов
- **Tests**:
  - backend: `pytest`, integration/e2e/unit
  - frontend: `vitest` + testing-library

## Ценность для бизнеса

ItemGate сокращает время на создание карточек товаров, повышает качество SEO-контента и снижает операционные издержки команды.
