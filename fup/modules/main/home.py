import random
from fup.core.module import ChangeModule


class Flat(ChangeModule):
    def __init__(self, start_expenses):
        self.expenses = start_expenses

    def next_year(self):
        inflation = self.get_prop("main.environment.Inflation", "inflation")
        self.expenses *= inflation
