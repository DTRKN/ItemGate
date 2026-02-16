#!/bin/bash
# Скрипт для автоматического бэкапа PostgreSQL базы данных

# Конфигурация
BACKUP_DIR="./backups"
DATE=$(date +"%Y%m%d_%H%M%S")
DB_CONTAINER="itemgate_postgres"
DB_NAME="itemgate_db"
DB_USER="itemgate_user"
BACKUP_FILE="${BACKUP_DIR}/backup_${DATE}.sql"

# Создаём директорию для бэкапов, если не существует
mkdir -p ${BACKUP_DIR}

echo "🔄 Начинаю бэкап базы данных ${DB_NAME}..."

# Создаём SQL дамп
docker exec -t ${DB_CONTAINER} pg_dump -U ${DB_USER} ${DB_NAME} > ${BACKUP_FILE}

if [ $? -eq 0 ]; then
    # Сжимаем бэкап
    gzip ${BACKUP_FILE}
    echo "✅ Бэкап успешно создан: ${BACKUP_FILE}.gz"
    
    # Удаляем бэкапы старше 7 дней
    find ${BACKUP_DIR} -name "backup_*.sql.gz" -mtime +7 -delete
    echo "🗑️  Старые бэкапы (>7 дней) удалены"
else
    echo "❌ Ошибка создания бэкапа"
    exit 1
fi

echo "📊 Текущие бэкапы:"
ls -lh ${BACKUP_DIR}
