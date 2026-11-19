"""assert-проверки главы I (раунды 1 и 2)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import chapter_1  # noqa: E402
from chapter_1 import ROUND_1, ROUND_2  # noqa: E402
from core import SYNTAX_ERROR_MESSAGE  # noqa: E402
from main import play_round  # noqa: E402

# ----------------------------- раунд 1 ------------------------------------


def test_r1_reference_pattern_accepted():
    ok, msg = ROUND_1.check(r"OE-[A-Z]{2}-[0-9]{3}")  # эталон из GDD
    assert ok, msg


def test_r1_other_correct_patterns_accepted():
    for pattern in (r"OE-[A-Z][A-Z]-\d\d\d",
                    r"OE-[A-Z]{2}-[0-9]{3}$",
                    r"^OE-(?:[A-Z]){2}-(?:[0-9]){3}$",
                    r"OE-[A-Z]{2}-\d{3}"):
        ok, msg = ROUND_1.check(pattern)
        assert ok, (pattern, msg)


def test_r1_wrong_prefix_rejected_with_prefix_message():
    ok, msg = ROUND_1.check(r"[A-Z]{2}-[A-Z]{2}-[0-9]{3}")
    assert not ok and chapter_1.T_PREFIX in msg and "OX-AR-104" in msg
    ok, msg = ROUND_1.check(r"[Oo][Ee]-[A-Z]{2}-[0-9]{3}")
    assert not ok and chapter_1.T_PREFIX in msg


def test_r1_cyrillic_prefix_gets_layout_note():
    ok, msg = ROUND_1.check(r"[OО][EЕ]-[A-Z]{2}-[0-9]{3}")  # кириллица в классах
    assert not ok and "кириллические" in msg


def test_r1_wrong_middle_rejected_with_middle_message():
    for pattern in (r"OE-[A-Za-z]{2}-[0-9]{3}",   # строчные
                    r"OE-[A-Z]+-[0-9]{3}",        # любое число букв
                    r"OE-[A-Z]{1,2}-[0-9]{3}"):
        ok, msg = ROUND_1.check(pattern)
        assert not ok and chapter_1.T_MIDDLE in msg, (pattern, msg)


def test_r1_wrong_digits_rejected_with_digits_message():
    for pattern in (r"OE-[A-Z]{2}-[0-9]+",
                    r"OE-[A-Z]{2}-[0-9]{3,4}",
                    r"OE-[A-Z]{2}-\w{3}"):
        ok, msg = ROUND_1.check(pattern)
        assert not ok and chapter_1.T_DIGITS in msg, (pattern, msg)


def test_r1_valid_ticket_rejected_gives_general_message():
    ok, msg = ROUND_1.check(r"OE-AB-123")
    assert not ok and chapter_1.T_GENERAL in msg and "OE-AR-104" in msg
    ok, msg = ROUND_1.check("")  # пустой шаблон тоже не роняет игру
    assert not ok and chapter_1.T_GENERAL in msg


def test_r1_syntax_error_does_not_crash():
    for pattern in ("OE-[A-Z{2}-[0-9]{3}", "(OE", "*OE", "OE-[A-Z]{2}-[0-9]{3}\\"):
        ok, msg = ROUND_1.check(pattern)
        assert not ok and msg == SYNTAX_ERROR_MESSAGE, pattern


# ----------------------------- раунд 2 ------------------------------------


def test_r2_correct_patterns_accepted():
    for pattern in (r"\bCASE-[0-9]{4}\b",
                    r"(?<![A-Za-z0-9])CASE-\d{4}(?![A-Za-z0-9])",
                    r"(?<!\w)CASE-[0-9]{4}(?!\w)"):
        ok, msg = ROUND_2.check(pattern)
        assert ok, (pattern, msg)


def test_r2_gdd_reference_pattern_passes_visible_document_only():
    # эталон из GDD верен на видимом документе, но «Обработка ошибок» требует
    # отклонять части повреждённых и более длинных кодов, поэтому без границ он не проходит
    import re
    ref = re.compile(r"CASE-[0-9]{4}")
    assert [m.group(0) for m in ref.finditer(chapter_1.JOURNAL)] == chapter_1.JOURNAL_IDS
    ok, msg = ROUND_2.check(r"CASE-[0-9]{4}")
    assert not ok


def test_r2_wrong_prefix_message():
    ok, msg = ROUND_2.check(r"[A-Za-z\u0400-\u04ff]{4}-[0-9]{4}\b")
    assert not ok and chapter_1.C_PREFIX in msg and "CASF-1111" in msg


def test_r2_cyrillic_prefix_gets_layout_note():
    ok, msg = ROUND_2.check(r"\b(?:CASE|\u0421\u0410SE)-[0-9]{4}\b")
    assert not ok and "кириллические" in msg


def test_r2_wrong_digits_message():
    ok, msg = ROUND_2.check(r"\bCASE-[0-9]+\b")
    assert not ok and chapter_1.C_DIGITS in msg and "CASE-123" in msg
    ok, msg = ROUND_2.check(r"\bCASE-\w{4}\b")  # буква вместо цифры
    assert not ok and chapter_1.C_DIGITS in msg


def test_r2_partial_match_shows_fragment_and_line():
    ok, msg = ROUND_2.check(r"CASE-[0-9]{4}(?![0-9])")  # нет границы слева/справа от букв
    assert not ok and chapter_1.C_PARTIAL in msg
    assert "Лишнее совпадение" in msg and "Строка:" in msg
    ok, msg = ROUND_2.check(r"[0-9]{4}")  # даты и обычные числа из журнала
    assert not ok and chapter_1.C_PARTIAL in msg and "1934" in msg


def test_r2_missing_codes_message_names_first_missing():
    ok, msg = ROUND_2.check(r"\bCASE-[1-9][0-9]{3}\b")  # не находит CASE-0001
    assert not ok and chapter_1.C_MISSING in msg and "CASE-0001" in msg
    ok, msg = ROUND_2.check(r"\bCASE-1042\b")
    assert not ok and chapter_1.C_MISSING in msg and "CASE-2081" in msg


def test_r2_syntax_error_does_not_crash():
    for pattern in (r"\bCASE-[0-9{4}\b", r"(CASE-[0-9]{4}", r"+CASE"):
        ok, msg = ROUND_2.check(pattern)
        assert not ok and msg == SYNTAX_ERROR_MESSAGE, pattern


# ------------------------- игровой цикл главы -----------------------------


def _io(answers):
    feed = iter(answers)
    log = []
    return (lambda prompt: next(feed)), log.append, log


def test_chapter_playthrough_with_hint_mistake_and_syntax_error():
    ask, say, log = _io(["?", "OE-[A-Z", "OE-[A-Z]+-[0-9]{3}",
                         r"OE-[A-Z]{2}-[0-9]{3}",
                         r"CASE-[0-9]{4}", r"\bCASE-[0-9]{4}\b"])
    for rnd in chapter_1.ROUNDS:
        assert play_round(rnd, ask, say) is True
    text = "\n".join(log)
    assert "Подсказка" in text and SYNTAX_ERROR_MESSAGE in text
    assert "OE-JM-421" in text and "CASE-4217" in text  # обе улики выданы


def test_exit_command_stops_round():
    ask, say, _ = _io(["выход"])
    assert play_round(ROUND_1, ask, say) is False
