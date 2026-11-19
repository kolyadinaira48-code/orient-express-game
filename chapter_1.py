"""Глава I. Список пассажиров (раунды 1 и 2).

Раунд 1: re.fullmatch(), билеты формата OE-XX-000.
Раунд 2: re.finditer(), номера дел формата CASE-0000.

Тексты сообщений об ошибках взяты из документа «Обработка ошибок».
Принимается ЛЮБОЙ шаблон, который верно проходит все тесты раунда.
"""
from collections import Counter

from characters import PASSENGERS
from core import CYRILLIC_NOTE, Round, fmt_list, has_cyrillic

TITLE = "Список пассажиров"
INTRO = ("Первая глава посвящена пассажирским документам: нужно проверить\n"
         "билеты и найти нужные регистрационные записи.")


def _cyr(*examples):
    """Приписка про раскладку, если среди примеров есть кириллица."""
    return CYRILLIC_NOTE if any(has_cyrillic(e) for e in examples) else ""


# ---------------------------------------------------------------------------
# Раунд 1. Поддельные билеты (re.fullmatch)
# ---------------------------------------------------------------------------

T_PREFIX = "Билет должен начинаться с OE- — две заглавные английские буквы и дефис."
T_MIDDLE = ("После OE- должны находиться ровно две заглавные английские буквы. "
            "Проверьте раскладку и количество букв.")
T_DIGITS = "В конце билета должны находиться ровно три цифры от 0 до 9."
T_GENERAL = ("Шаблон не распознаёт все билеты установленного формата. "
             "Проверьте дефисы и количество символов в каждой части.")

VALID_TICKETS = [p.ticket for p in PASSENGERS]
HIDDEN_VALID_TICKETS = ["OE-AB-123", "OE-ZZ-000", "OE-XY-999", "OE-QA-010"]

# Поддельные билеты по видам ошибки. Порядок групп = приоритет сообщений.
FAKE_PREFIX = [
    "OX-AR-104",            # изменён префикс
    "oe-AR-104",            # строчные буквы
    "Oe-AR-104",            # неверный регистр
    "\u041eE-AR-104",       # первая буква кириллическая О
    "O\u0415-AR-104",       # вторая буква кириллическая Е
    "XOE-AR-104",           # лишний символ перед префиксом
    "E-AR-104",             # префикс неполный
    "AR-104",               # префикса нет
]
FAKE_MIDDLE = [
    "OE-ar-104",            # строчные (пример из GDD)
    "OE-ABC-421",           # три буквы (пример из GDD)
    "OE-A-104",             # одна буква
    "OE-Ar-104",            # неверный регистр
    "OE-\u0410\u0412-104",  # кириллические А и В
    "OE-A1-104",            # цифра вместо буквы
    "OE--104",              # букв нет
]
FAKE_DIGITS = [
    "OE-JM-42",             # две цифры (пример из GDD)
    "OE-TH-6137",           # четыре цифры (пример из GDD)
    "OE-AB-12",
    "OE-AB-12A",            # буква вместо цифры
    "OE-AB-1234",
    "OE-AB-ABC",
    "OE-AB-",
    "OE-AB-104X",           # лишний символ после цифр
]
INVALID_GROUPS = [(T_PREFIX, FAKE_PREFIX), (T_MIDDLE, FAKE_MIDDLE),
                  (T_DIGITS, FAKE_DIGITS)]
VISIBLE_FAKE_TICKETS = ["OE-JM-42", "OE-ar-104", "OE-ABC-421", "OE-TH-6137"]


class TicketRound(Round):
    """Игрок описывает формат билета; проверка через re.fullmatch()."""

    def __init__(self, *args, valid, invalid_groups, **kwargs):
        super().__init__(*args, **kwargs)
        self.valid = valid
        self.invalid_groups = invalid_groups

    def evaluate(self, compiled):
        # 1. Поддельный билет принят: ошибку можно назвать точно (подтверждена тестом).
        for message, tickets in self.invalid_groups:
            for ticket in tickets:
                if compiled.fullmatch(ticket):
                    return False, (f"Ваш шаблон принял поддельный билет {ticket!r}."
                                   f"{_cyr(ticket)}\n{message}")
        # 2. Настоящий билет отвергнут: причина неоднозначна, даём общую подсказку.
        for ticket in self.valid:
            if not compiled.fullmatch(ticket):
                return False, (f"Ваш шаблон отверг настоящий билет {ticket!r}.\n"
                               f"{T_GENERAL}")
        return True, ("Задание выполнено! Шаблон принимает все билеты установленного "
                      "формата и отклоняет поддельные.")


ROUND_1 = TicketRound(
    1,
    "Поддельные билеты",
    story=("Детектив обнаружил несколько пассажирских билетов и фрагментов документов.\n"
           "Некоторые записи могут быть повреждены или содержать ошибки. Нужно\n"
           "определить, какие билеты соответствуют установленному формату."),
    task=("найдите регулярное выражение, которое принимает только билеты формата\n"
          "OE-XX-000: OE- — постоянный префикс, XX — две заглавные английские\n"
          "буквы, 000 — три цифры. Шаблон проверяется на всей строке целиком."),
    shown=("Правильные примеры:   " + ", ".join(VALID_TICKETS) + "\n"
           "Неправильные примеры: " + ", ".join(VISIBLE_FAKE_TICKETS)),
    clue=("Среди документов находится повреждённый фрагмент OE-JM-42, найденный возле\n"
          "служебного коридора. В списке пассажиров обнаружен билет OE-JM-421,\n"
          "принадлежащий Джулиану Мерсеру. Это первая зацепка, но ещё не доказательство\n"
          "его причастности."),
    hints=[
        "Для проверки количества символов используются фигурные скобки: "
        "{n} означает ровно n повторений.",
        "Билет состоит из частей: постоянный префикс OE-, две буквы, дефис, три цифры. "
        "Опишите каждую часть отдельно: для букв подойдёт диапазон [A-Z], "
        "для цифр — [0-9].",
        "Структура: OE-, затем два символа-буквы, дефис, затем три символа-цифры. "
        "Проверка идёт через fullmatch, поэтому ^ и $ не нужны.",
    ],
    valid=VALID_TICKETS + HIDDEN_VALID_TICKETS,
    invalid_groups=INVALID_GROUPS,
)


# ---------------------------------------------------------------------------
# Раунд 2. Пассажирские записи (re.finditer)
# ---------------------------------------------------------------------------

C_PREFIX = "Идентификатор должен начинаться с CASE — четыре заглавные английские буквы."
C_DIGITS = "После CASE- должны находиться ровно четыре цифры от 0 до 9."
C_PARTIAL = ("Найдены лишние фрагменты. Извлекайте целый идентификатор CASE-0000, "
             "а не его часть.")
C_MISSING = "Не все номера пассажирских дел найдены. Проверьте формат CASE-0000."

JOURNAL = (
    "ПАССАЖИРСКИЙ РЕГИСТРАЦИОННЫЙ ЖУРНАЛ\n\n"
    "Дата оформления: 18.11.1934\n\n"
    + "\n".join(f"{p.name_en} — {p.case_id}" for p in PASSENGERS)
    + "\n\nКоличество пассажиров: 8\nВремя последней проверки: 22:35"
)
JOURNAL_IDS = [p.case_id for p in PASSENGERS]

# Скрытые документы: (категория сообщения при лишних совпадениях, текст, ожидаемый список).
HIDDEN_DOCS = [
    # --- изменённый, строчный или кириллический префикс ---
    ("prefix",
     "ЖУРНАЛ, СТРАНИЦА 2\n"
     "Rene Dupont — CASF-1111\n"
     "Anna Weber — case-2222\n"
     "Karl Brandt — Case-3333\n"
     "Lucia Rossi — \u0421\u0410SE-4444\n"      # кириллические С и А
     "Piotr Nowak — CAS-6666\n"
     "Hans Vogel — CASE-5555\n"
     "Eva Berg — CASE-7777",
     ["CASE-5555", "CASE-7777"]),
    # --- неверное число цифр или нецифровой символ ---
    ("digits",
     "ЖУРНАЛ, СТРАНИЦА 3\n"
     "Ivan Petrov — CASE-123\n"
     "Marta Klein — CASE-12345\n"
     "Otto Berg — CASE-12A4\n"
     "Nina Rossi — CASE-0001\n"
     "Paul Gray — CASE-9999",
     ["CASE-0001", "CASE-9999"]),
    ("digits",
     "ЖУРНАЛ, СТРАНИЦА 4\n"
     "CASE-12, CASE-123456, CASE-ABCD, CASE-2026.",
     ["CASE-2026"]),
    # --- части повреждённых кодов, даты и обычные числа ---
    ("partial",
     "РЕГИСТРАЦИЯ ОТ 12.03.1934\n"
     "Номер вагона: 1042\n"
     "Купе № 7, время 23:05\n"
     "CASE-4217 — Julian Mercer\n"
     "Итого: 8 пассажиров, сумма 2081 франк.",
     ["CASE-4217"]),
    ("partial",
     "XCASE-1042 CASE-2081X 7CASE-3175 CASE-4217\n"
     "CASE-5092, (CASE-6134) и CASE-7226.",
     ["CASE-4217", "CASE-5092", "CASE-6134", "CASE-7226"]),
    # --- повторы и порядок ---
    ("partial",
     "CASE-1111, CASE-2222 и снова CASE-1111.",
     ["CASE-1111", "CASE-2222", "CASE-1111"]),
]


def _line_with(text, fragment):
    for line in text.splitlines():
        if fragment in line:
            return line
    return text.splitlines()[0] if text else ""


class RecordsRound(Round):
    """Игрок находит все номера дел; проверка через re.finditer()."""

    def __init__(self, *args, document, expected, hidden_docs, **kwargs):
        super().__init__(*args, **kwargs)
        self.docs = [("partial", document, expected)] + hidden_docs
        self.messages = {"prefix": C_PREFIX, "digits": C_DIGITS, "partial": C_PARTIAL}

    def evaluate(self, compiled):
        for category, text, expected in self.docs:
            got = [m.group(0) for m in compiled.finditer(text)]
            if got == expected:
                continue
            extra = list((Counter(got) - Counter(expected)).elements())
            missing = list((Counter(expected) - Counter(got)).elements())
            if extra:
                # Лишнее в списке: сообщение по виду документа + строка-источник.
                fragment = next(g for g in got if g in extra)
                return False, (f"{self.messages[category]}{_cyr(fragment)}\n"
                               f"Лишнее совпадение: {fragment!r}\n"
                               f"Строка: {_line_with(text, fragment)!r}")
            if missing:
                return False, (f"{C_MISSING}\n"
                               f"Первый пропущенный идентификатор: {missing[0]!r}\n"
                               f"Строка: {_line_with(text, missing[0])!r}")
            return False, ("Набор совпадений верный, но порядок или число повторов "
                           f"отличается.\nОжидалось: {fmt_list(expected)}\n"
                           f"Найдено:   {fmt_list(got)}")
        return True, ("Задание выполнено! Найдены все номера дел, и нет ни одного "
                      "лишнего фрагмента.")


ROUND_2 = RecordsRound(
    2,
    "Пассажирские записи",
    story=("В архиве поезда обнаружен регистрационный журнал с номерами пассажирских\n"
           "дел, датами, временем и обычными числовыми записями."),
    task=("найдите все идентификаторы формата CASE-0000: CASE-, затем ровно четыре\n"
          "цифры. Идентификатор должен быть целым: если вплотную к нему стоят другие\n"
          "буквы или цифры, это повреждённая запись, а не номер дела."),
    shown=("Документ:\n" + "\n".join("  " + line for line in JOURNAL.splitlines())
           + "\n\nНужно найти (по порядку): " + fmt_list(JOURNAL_IDS)),
    clue=("Среди архивных записей обнаруживается отдельный запрос на получение дела\n"
          "CASE-4217, принадлежащего Джулиану Мерсеру. Запрос был сделан незадолго\n"
          "до происшествия; причина пока неизвестна."),
    hints=[
        "Здесь не проверка всей строки, а поиск внутри текста. Опишите "
        "идентификатор: постоянная часть CASE-, затем цифры с точным "
        "количеством повторений.",
        "Идентификатор не должен быть частью более длинного слова или числа. "
        "Для этого подойдёт граница слова \\b: она ставится по краям шаблона.",
        "Структура: граница, CASE-, четыре цифры [0-9]{4}, граница.",
    ],
    document=JOURNAL,
    expected=JOURNAL_IDS,
    hidden_docs=HIDDEN_DOCS,
)

ROUNDS = [ROUND_1, ROUND_2]

# Отдельные функции проверки по требованию GDD (раздел 8.4)
check_round_1 = ROUND_1.check
check_round_2 = ROUND_2.check
