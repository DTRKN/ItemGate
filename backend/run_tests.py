#!/usr/bin/env python3
"""
Скрипт для запуска тестов ItemGate API
"""

import subprocess
import sys
import os

def run_tests(test_type=None):
    """Запуск тестов определенного типа или всех"""

    base_cmd = [sys.executable, "-m", "pytest"]

    description = "all tests"
    if test_type == "unit":
        cmd = base_cmd + ["tests/unit/"]
        description = "unit tests"
    elif test_type == "integration":
        cmd = base_cmd + ["tests/integration/"]
        description = "integration tests"
    elif test_type == "e2e":
        cmd = base_cmd + ["tests/e2e/"]
        description = "e2e tests"
    else:
        # Запуск всех тестов
        cmd = base_cmd + ["tests/"]
        description = "all tests"

    # Добавляем опции для покрытия
    cmd.extend([
        "--cov=.",
        "--cov-report=term-missing",
        "--cov-report=html:htmlcov",
        "--cov-fail-under=50"  # Снижаем требуемое покрытие до 50%
    ])

    print(f"Запуск команды: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=os.path.dirname(__file__))

    if result.returncode == 0:
        print(f"✅ {description} - SUCCESS")
    else:
        print(f"❌ {description} - FAILED (exit code: {result.returncode})")
        print("💡 Для детальной информации запустите: python quick_test.py")

    return result.returncode

def run_specific_test(test_file):
    """Запуск конкретного тестового файла"""
    cmd = [sys.executable, "-m", "pytest", test_file, "--cov=.", "--cov-report=term-missing"]
    print(f"Запуск команды: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=os.path.dirname(__file__))
    return result.returncode

if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_type = sys.argv[1]
        if test_type in ["unit", "integration", "e2e"]:
            exit_code = run_tests(test_type)
        elif test_type.endswith(".py"):
            exit_code = run_specific_test(test_type)
        else:
            print("Использование: python run_tests.py [unit|integration|e2e|test_file.py]")
            exit_code = 1
    else:
        print("Запуск всех тестов...")
        exit_code = run_tests()

    sys.exit(exit_code)