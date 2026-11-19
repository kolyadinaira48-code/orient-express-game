import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core import SYNTAX_ERROR_MESSAGE
from chapter_3 import ROUND_5, ROUND_6


def test_round_5():
    # эталонный шаблон принимается
    ok, _ = ROUND_5.check(r"BAG-[A-Z]{2}-[0-9]{3}")
    assert ok
    # второй верный шаблон принимается
    ok, _ = ROUND_5.check(r"BAG-[A-Z]{2}-\d{3}")
    assert ok
    # неверный: принимает лишние символы в конце
    ok, msg = ROUND_5.check(r".*BAG-[A-Z]{2}-[0-9]{3}")
    assert not ok and "целиком" in msg
    # неверный: принимает произвольный префикс
    ok, msg = ROUND_5.check(r"[A-Z]{3}-[A-Z]{2}-[0-9]{3}")
    assert not ok and "BAG" in msg
    # неверный: принимает строчные буквы
    ok, msg = ROUND_5.check(r"BAG-[A-Za-z]{2}-[0-9]{3}")
    assert not ok and "заглавные" in msg
    # неверный: принимает буквы вместо цифр
    ok, msg = ROUND_5.check(r"BAG-[A-Z]{2}-[0-9A-Z]{3}")
    assert not ok and "цифры" in msg
    # синтаксическая ошибка не роняет игру
    ok, msg = ROUND_5.check("[A-Z")
    assert not ok and msg == SYNTAX_ERROR_MESSAGE


def test_round_6():
    # эталонный шаблон принимается
    ok, _ = ROUND_6.check(r"(?:CASE-[0-9]{4}|BAG-[A-Z]{2}-[0-9]{3})")
    assert ok
    # второй верный шаблон принимается
    ok, _ = ROUND_6.check(r"CASE-[0-9]{4}|BAG-[A-Z]{2}-[0-9]{3}")
    assert ok
    # неверный: скрывает только CASE
    ok, msg = ROUND_6.check(r"CASE-[0-9]{4}")
    assert not ok and "остался" in msg
    # неверный: скрывает только BAG
    ok, msg = ROUND_6.check(r"BAG-[A-Z]{2}-[0-9]{3}")
    assert not ok and "остался" in msg
    # синтаксическая ошибка
    ok, msg = ROUND_6.check("[")
    assert not ok and msg == SYNTAX_ERROR_MESSAGE


if __name__ == "__main__":
    test_round_5()
    test_round_6()
    print("Тесты главы III пройдены!")