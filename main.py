"""Убийство в Восточном экспрессе: Последнее путешествие.

Запуск: python main.py
Главы подключаются автоматически, если их файл есть в проекте.
"""
from importlib import import_module

import story

CHAPTER_MODULES = ["chapter_1", "chapter_2", "chapter_3"]
PROMPT = "Введите регулярное выражение: "
HELP = ("Команды: ? — подсказка, выход — завершить игру.\n"
        "Шаблон вводится как есть, без кавычек и префикса r.")


def load_chapters():
    chapters = []
    for name in CHAPTER_MODULES:
        try:
            chapters.append(import_module(name))
        except ModuleNotFoundError as err:
            if err.name != name:
                raise
    return chapters


def play_round(rnd, ask=input, say=print):
    """Проводит раунд. True — решён, False — игрок вышел."""
    say(rnd.intro())
    hints_used = 0
    mistakes = 0
    while True:
        raw = ask(PROMPT)
        command = raw.strip().lower()
        if command in ("выход", "exit", "quit"):
            return False
        if command in ("?", "подсказка"):
            say(rnd.hint(hints_used))
            hints_used += 1
            continue
        success, message = rnd.check(raw)
        say(message)
        if success:
            say(f"\nНовая улика: {rnd.clue}")
            return True
        mistakes += 1
        say("Попробуйте ещё раз." + (" Введите ? для подсказки." if mistakes >= 2 else ""))


def run_game(chapters=None, ask=input, say=print):
    chapters = load_chapters() if chapters is None else chapters
    if not chapters:
        say("Не найдено ни одной главы.")
        return False
    say(f"{'=' * 60}\n{story.GAME_TITLE}\n{'=' * 60}\n{story.INTRO}\n\n{HELP}")
    journal = []  # журнал расследования
    try:
        for index, chapter in enumerate(chapters, 1):
            say(f"\n=== Глава {chapter.TITLE} ===\n{chapter.INTRO}")
            for rnd in chapter.ROUNDS:
                if not play_round(rnd, ask, say):
                    say("\nРасследование прервано.")
                    return False
                journal.append(rnd.clue)
            say(f"\nГлава «{chapter.TITLE}» завершена.")
    except (EOFError, KeyboardInterrupt):
        say("\n\nРасследование прервано.")
        return False
    say("\n=== Журнал улик ===")
    for i, clue in enumerate(journal, 1):
        say(f"{i}. {clue}")
    finale = next((c.finale for c in chapters if hasattr(c, "finale")), None)
    if finale:
        finale(ask, say, journal)  # выбор подозреваемого (автор главы III)
    return True


if __name__ == "__main__":
    run_game()
