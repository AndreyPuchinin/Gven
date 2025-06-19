from BaseLogger import Logger


class JsonFileLogger(Logger):
    def __init__(self, logger_name: str):
        super().__init__(logger_name)
        self.format_error_text = \
            "❌ Повреждение Базы Данных! Дальнейшее использование невозможно без исправления на сервере!"

    def FormatError(self):
        self.add_uniq_error(self.format_error_text)

    def FormatIsCorrect(self):
        while self.format_error_text in  self._errors:
            self._errors.remove(self.format_error_text)


class ProjLogger(Logger):
    def NoProject(self):
        error_text = "❌ Сначала создайте проект!"
        self.add_uniq_error(error_text)


class TimeEntryLogger(Logger):
    def EntryFormatError(self):
        error_text = "❌ Неверный формат времени! Пример: <code>01.01.2025 12:30</code>"
        self.add_uniq_error(error_text)