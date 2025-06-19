from datetime import datetime


def get_current_time_in_formats():
    """Возвращает текущие дату и время в двух форматах:
    - Полный: yyyy.mm.dd hh.mm (например, 2025.06.19 19.19)
    - Сокращённый: yy.m.d h.m (например, 25.6.19 7.7)
    """
    now = datetime.now()

    # Полный формат (2025.06.19 19.19)
    full_format = now.strftime("%Y.%m.%d %H.%M")

    # Сокращённый формат даты (25.6.19)
    short_date = now.strftime("%y.{}.%d").format(now.month)  # Убираем нули через форматирование
    short_date = short_date.replace(".0", ".")

    # Сокращённый формат времени (12-часовой + без нулей)
    hour_12h = int(now.strftime("%I"))  # Часы в 12-часовом формате (1-12)
    minute = int(now.strftime("%M"))  # Минуты (0-59)

    short_time = f"{hour_12h}.{minute}"

    short_format = f"{short_date} {short_time}"

    return {
        "full_format": full_format,
        "short_format": short_format,
    }


# Пример использования
# current_time = get_current_time_in_formats()
# print("Полный формат:", current_time["full_format"])
# print("Сокращённый формат:", current_time["short_format"])


import re

# Основная регулярка для даты/времени (ваш вариант + доработка)
datetime_pattern = r"\d{2,4}\.\d{1,2}\.\d{1,2} \d{1,2}\.\d{1,2}"

# Список всех тегов Telegram (открывающие и закрывающие)
tg_tags = ["b", "i", "u", "s", "code", "pre", "tg-spoiler"]
tags_pattern = "|".join(tg_tags)  # Объединяем через | для выбора

# Регулярка для одного уровня вложенности (например, <b>...</b>)
single_tag_wrap = r"(?:<({tags})>.*?</\1>)".format(tags=tags_pattern)

# Рекурсивная регулярка для любых комбинаций тегов
nested_tags_pattern = r"(?:<({tags})>(?:{datetime}|.*?)*?</\1>)".format(
    tags=tags_pattern,
    datetime=datetime_pattern
)

# Финальная регулярка:
# 1. Ищет дату/время БЕЗ тегов ИЛИ
# 2. Дату/время, обёрнутую в любые комбинации тегов
final_regex = re.compile(
    r"^(?:{datetime}|(?:{nested_tags})+)$".format(
        datetime=datetime_pattern,
        nested_tags=nested_tags_pattern
    ),
    re.DOTALL  # Чтобы .*? захватывал переносы строк
)

# Примеры валидных строк:
# valid_examples = [
#     "2025.06.19 19.19",                     # Без тегов
#     "<i>25.6.19 7.7</i>",                   # Один тег
#     "<b><code>2025.06.19 19.19</code></b>", # Вложенные теги
#     "<pre><u>25.6.19 7.7</u></pre>",
#     "<tg-spoiler><b>2025.06.19 19.19</b></tg-spoiler>"
# ]

# Проверка
# for example in valid_examples:
#     print(f"'{example}': {bool(final_regex.fullmatch(example))}")