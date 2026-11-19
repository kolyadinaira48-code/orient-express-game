# Глава I: ветка, PR и демонстрация

## Что в main до начала работы

`README.md`, `main.py`, `core.py`, `characters.py`, `story.py`, `run_tests.py`,
`tests/__init__.py`, `.gitignore`. Файлы глав в main добавляются через pull request.

## Ваша ветка

```
git switch main
git pull origin main
git switch -c feature/chapter-1
git add chapter_1.py
git commit -m "Добавить главу I: раунды 1 и 2"
git add tests/test_chapter_1.py
git commit -m "Добавить assert-проверки главы I"
git push -u origin feature/chapter-1
```

Затем pull request `feature/chapter-1 → main`, проверяющий назначается в Reviewers.
В описании: какие раунды добавлены и как проверить (`python main.py`, ввести
`[A-Z]+-[0-9]{3}`, затем `OE-[A-Z]{2}-[0-9]{3}`; `python run_tests.py`).

## Проверка чужой ветки

```
git fetch origin
git switch feature/chapter-2
python main.py
python run_tests.py
```

В комментарии к PR: какой верный и какой неверный шаблон введены, что ответила игра.

## Демонстрация: изменение одного правила

| Раунд | Верный шаблон | Если правило изменится |
|---|---|---|
| 1 | `OE-[A-Z]{2}-[0-9]{3}` | четыре цифры: `{4}` в конце; префикс `TR-`: заменить `OE-` |
| 2 | `CASE-[0-9]{4}` | пять цифр: `{5}`; префикс `FILE`: заменить `CASE` |
