"""Общий интерфейс раунда (согласован всеми участниками команды).

Каждый раунд — объект с методом check(pattern) -> (успех: bool, сообщение: str).
Игровой цикл (main.py) вызывает только intro(), hint(), check() и читает clue,
поэтому раунды всех глав запускаются одинаково.
"""
import re
from abc import ABC, abstractmethod

# Сообщение из документа «Обработка ошибок», общая ошибка синтаксиса.
SYNTAX_ERROR_MESSAGE = ("В регулярном выражении обнаружена синтаксическая ошибка. "
                        "Проверьте скобки, квадратные скобки и специальные символы.")


def fmt_list(items, limit=10):
    """Вывод списка строк; длинные списки обрезаются."""
    if not items:
        return "[] (пусто)"
    text = ", ".join(repr(x) for x in items[:limit])
    if len(items) > limit:
        text += f", … ещё {len(items) - limit}"
    return "[" + text + "]"


def has_cyrillic(text):
    return any("\u0400" <= ch <= "\u04ff" for ch in text)


CYRILLIC_NOTE = (" В этом фрагменте есть кириллические буквы, которые внешне "
                 "похожи на латинские: проверьте раскладку.")


class Round(ABC):
    """Один раунд расследования."""

    def __init__(self, number, title, story, task, shown, clue, hints):
        self.number = number   # сквозной номер раунда (1–6)
        self.title = title     # название раунда
        self.story = story     # сюжетная ситуация
        self.task = task       # задание игроку
        self.shown = shown     # документ и примеры, видимые игроку
        self.clue = clue       # улика за успешное решение
        self.hints = hints     # подсказки от общей к конкретной

    def intro(self):
        return (f"\n--- Раунд {self.number}. {self.title} ---\n\n"
                f"{self.story}\n\nЗадание: {self.task}\n\n{self.shown}\n")

    def hint(self, level):
        return "Подсказка: " + self.hints[min(level, len(self.hints) - 1)]

    def check(self, pattern):
        """Возвращает (успех, сообщение). Синтаксическая ошибка не роняет игру."""
        try:
            compiled = re.compile(pattern)
        except (re.error, OverflowError, RecursionError):
            return False, SYNTAX_ERROR_MESSAGE  # тесты раунда не запускаются
        return self.evaluate(compiled)

    @abstractmethod
    def evaluate(self, compiled):
        """Проверка скомпилированного шаблона: (успех, сообщение)."""
