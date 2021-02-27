from fup.core.module import Module


class OtherExpenses(Module):
    def __init__(self, manager):
        super().__init__(manager)
        self.expenses = manager.config["other_expenses"]

    def next_year(self):
        inflation = self.get_prop("main.environment.Inflation", "inflation")

        self.expenses *= inflation
        self.add_expenses(self.expenses)


class LuxuryExpenses(Module):
    def __init__(self, manager):
        super().__init__(manager)
        self.expenses = manager.config["luxury_expenses"]

    def next_year(self):
        inflation = self.get_prop("main.environment.Inflation", "inflation")
        self.expenses *= inflation
        self.add_expenses(self.expenses)
