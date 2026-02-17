#!/usr/bin/env python3
"""
Быстрый запуск тестов без покрытия для проверки исправлений
"""

import subprocess
import sys
import os


def run_stage(backend_dir, title, test_path, timeout=240):
    print(f"\n{title}", flush=True)
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest",
            test_path,
            "-v",
            "--tb=short"
        ], cwd=backend_dir, capture_output=False, timeout=timeout)
        return result.returncode
    except subprocess.TimeoutExpired:
        print(f"⏱ Таймаут этапа {title} ({timeout}с). Переходим дальше.", flush=True)
        return 124

def run_quick_tests():
    """Быстрый запуск тестов без покрытия"""
    backend_dir = os.path.dirname(__file__)

    print("🚀 Быстрый запуск тестов (без покрытия)")
    print("=" * 50)

    # Запуск unit / integration / e2e тестов
    result_unit = run_stage(backend_dir, "📋 Unit тесты:", "tests/unit/", timeout=240)
    result_integration = run_stage(backend_dir, "🔗 Integration тесты:", "tests/integration/", timeout=300)
    result_e2e = run_stage(backend_dir, "🌐 E2E тесты:", "tests/e2e/", timeout=300)

    # Итоги
    print("\n" + "=" * 50)
    print("📊 ИТОГИ БЫСТРОГО ЗАПУСКА")

    results = [result_unit, result_integration, result_e2e]
    test_types = ["Unit", "Integration", "E2E"]

    all_passed = True
    for i, code in enumerate(results):
        status = "✅ ПРОЙДЕН" if code == 0 else "❌ ПРОВАЛЕН"
        print(f"{test_types[i]}: {status}")
        if code != 0:
            all_passed = False

    print("=" * 50)
    if all_passed:
        print("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ!")
        return 0
    else:
        print("💥 НЕКОТОРЫЕ ТЕСТЫ ПРОВАЛЕНЫ!")
        return 1

if __name__ == "__main__":
    exit_code = run_quick_tests()
    sys.exit(exit_code)