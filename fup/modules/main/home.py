import random
from fup.core.module import Module


class Flat(Module):
    def __init__(self, manager):
        super().__init__(manager)
        self.expenses = manager.config["flat_expenses"]

    def next_year(self):
        inflation = self.get_prop("main.environment.Inflation", "inflation")
        self.expenses *= inflation
        self.add_expenses(self.expenses)
