"""Запуск всех проверок без pytest: python run_tests.py"""
import importlib
import pkgutil
import sys

import tests

failed = total = 0
for info in pkgutil.iter_modules(tests.__path__):
    if not info.name.startswith("test_"):
        continue
    module = importlib.import_module(f"tests.{info.name}")
    for name in sorted(dir(module)):
        if name.startswith("test_"):
            total += 1
            try:
                getattr(module, name)()
                print(f"ok    {info.name}.{name}")
            except Exception as err:  # noqa: BLE001
                failed += 1
                print(f"FAIL  {info.name}.{name}: {type(err).__name__}: {err}")
print(f"\nПроверок: {total}, провалено: {failed}")
sys.exit(1 if failed else 0)
