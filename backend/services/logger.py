import logging
import sys
from pathlib import Path
from datetime import datetime

# Создаём директорию для логов
LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

# Настройка формата логов
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Настройка обработчиков
def setup_logging():
    """Настройка системы логирования"""
    
    # Основной logger
    logger = logging.getLogger("itemgate")
    logger.setLevel(logging.DEBUG)
    
    # Очищаем существующие обработчики
    logger.handlers.clear()
    
    # === Консольный вывод ===
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # === Файловый вывод (все логи) ===
    log_file = LOG_DIR / f"app_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    # === Файловый вывод (только ошибки) ===
    error_log = LOG_DIR / f"errors_{datetime.now().strftime('%Y%m%d')}.log"
    error_handler = logging.FileHandler(error_log, encoding='utf-8')
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(file_formatter)
    logger.addHandler(error_handler)
    
    # Настраиваем корневой логгер для всех модулей
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    
    return logger

# Инициализируем logger
logger = setup_logging()

def log_info(message: str):
    """Логирование информации"""
    logger.info(message)

def log_error(message: str, exc_info=None):
    """Логирование ошибок"""
    logger.error(message, exc_info=exc_info)

def log_warning(message: str):
    """Логирование предупреждений"""
    logger.warning(message)

def log_debug(message: str):
    """Логирование отладочной информации"""
    logger.debug(message)
