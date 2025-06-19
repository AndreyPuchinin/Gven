from abc import ABC


class Logger(ABC):
    def __init__(self, logger_name: str):
        self.logger_name = logger_name
        self._notes = []
        self._errors = []
        self._warnings = []
        self._msgs = []

    def add_error(self, new_error: str) -> None:
        self._errors += [new_error]

    def add_warning(self, new_warning: str) -> None:
        self._warnings += [new_warning]

    def add_note(self, new_note) -> None:
        self._notes += [new_note]

    def add_msg(self, new_msg) -> None:
        self._msgs += [new_msg]

    def add_uniq_error(self, new_error: str) -> None:
        if new_error not in self._errors:
            self._errors += [new_error]

    def add_uniq_warning(self, new_warning: str) -> None:
        if new_warning not in self._warnings:
            self._warnings += [new_warning]

    def add_uniq_note(self, new_note) -> None:
        if new_note not in self._notes:
            self._notes += [new_note]

    def add_uniq_msg(self, new_msg) -> None:
        if new_msg not in self._msgs:
            self._msgs += [new_msg]

    def get_correctness(self) -> bool:
        if not self._errors and not self._warnings:
            return True
        return False

    def print_one(self, anythings: list) -> bool:
        if anythings:
            for one_msg in anythings:
                print(one_msg)
        return self.get_correctness()

    def print_all(self) -> bool:
        print(self.logger_name + ':')
        self.print_one(self._errors)
        self.print_one(self._warnings)
        self.print_one(self._notes)
        self.print_one(self._msgs)
        if not self._errors and \
                not self._warnings and \
                not self._notes:
            print('success!')
        print()
        return self.get_correctness()

    def __del__(self):
        self.print_all()