import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from chapter_2 import ROUND_3, ROUND_4
from core import SYNTAX_ERROR_MESSAGE


def test_r3_reference_pattern_accepted():
    ok, _ = ROUND_3.check(r"MSG-[A-Z]{2}-[0-9]{3}")
    assert ok, "Эталонный шаблон должен приниматься"


def test_r3_other_correct_patterns_accepted():
    ok, _ = ROUND_3.check(r"MSG-[A-Z][A-Z]-\d\d\d")
    assert ok, "Альтернативный верный шаблон должен приниматься"


def test_r3_wrong_middle_rejected():
    ok, msg = ROUND_3.check(r"MSG-[A-Z]+-[0-9]{3}")
    assert not ok, "Шаблон с + должен отклоняться"
    assert "лишний код" in msg.lower() or "ровно две" in msg.lower()


def test_r3_syntax_error_does_not_crash():
    ok, msg = ROUND_3.check(r"MSG-[A-Z")
    assert not ok
    assert msg == SYNTAX_ERROR_MESSAGE


def test_r4_reference_pattern_accepted():
    ok, _ = ROUND_4.check(r"(?<=СВИДЕТЕЛЬ: )[А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+")
    assert ok, "Эталонный шаблон с просмотром назад должен приниматься"


def test_r4_wrong_format_rejected():
    ok, msg = ROUND_4.check(r"СВИДЕТЕЛЬ: [А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+")
    assert not ok
    assert "Метка СВИДЕТЕЛЬ:" in msg


def test_r4_syntax_error_does_not_crash():
    ok, msg = ROUND_4.check(r"[А-ЯЁ")
    assert not ok
    assert msg == SYNTAX_ERROR_MESSAGE