# Multi-stage build для оптимизации размера образа
FROM python:3.11-slim as builder

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Копируем requirements и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# === Финальный образ ===
FROM python:3.11-slim

WORKDIR /app

# Устанавливаем PostgreSQL клиент
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Копируем установленные пакеты из builder
COPY --from=builder /root/.local /root/.local

# Убеждаемся, что скрипты из pip доступны в PATH
ENV PATH=/root/.local/bin:$PATH

# Копируем весь код приложения
COPY . .

# Создаём директории для логов и данных
RUN mkdir -p logs data

# Expose порт
EXPOSE 8000

# Команда запуска
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
