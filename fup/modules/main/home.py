import random
from fup.core.module import ChangeModule


class Flat(ChangeModule):
    def __init__(self, manager, start_expenses):
        super().__init__(manager)
        self.expenses = start_expenses

    def next_year(self):
        inflation = self.get_prop("main.environment.Inflation", "inflation")
        self.expenses *= inflation
