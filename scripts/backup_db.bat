@echo off
REM Скрипт для автоматического бэкапа PostgreSQL базы данных (Windows)

SET BACKUP_DIR=.\backups
SET DB_CONTAINER=itemgate_postgres
SET DB_NAME=itemgate_db
SET DB_USER=itemgate_user

REM Создаём имя файла с датой и временем
FOR /f "tokens=2-4 delims=/ " %%a IN ('date /t') DO (SET mydate=%%c%%a%%b)
FOR /f "tokens=1-2 delims=/:" %%a IN ('time /t') DO (SET mytime=%%a%%b)
SET BACKUP_FILE=%BACKUP_DIR%\backup_%mydate%_%mytime%.sql

REM Создаём директорию для бэкапов
IF NOT EXIST %BACKUP_DIR% mkdir %BACKUP_DIR%

echo 🔄 Начинаю бэкап базы данных %DB_NAME%...

REM Создаём SQL дамп
docker exec -t %DB_CONTAINER% pg_dump -U %DB_USER% %DB_NAME% > %BACKUP_FILE%

IF %ERRORLEVEL% EQU 0 (
    echo ✅ Бэкап успешно создан: %BACKUP_FILE%
) ELSE (
    echo ❌ Ошибка создания бэкапа
    exit /b 1
)

echo 📊 Текущие бэкапы:
dir /B %BACKUP_DIR%
