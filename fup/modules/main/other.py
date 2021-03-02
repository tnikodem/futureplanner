from fup.core.module import Module


class OtherExpenses(Module):
    def __init__(self, manager):
        super().__init__(manager)
        self.expenses = manager.config["other_expenses"]

    def next_year(self):
        total_inflation = self.get_prop("main.environment.Inflation", "total_inflation")
        self.expenses = total_inflation * self.manager.config["other_expenses"]
        if self.profile.luxury_level == 0:
            self.expenses *= 0
        self.add_expenses(self.expenses)


class LuxuryExpenses(Module):
    def __init__(self, manager):
        super().__init__(manager)
        self.expenses = manager.config["other_expenses"]

    def next_year(self):
        total_inflation = self.get_prop("main.environment.Inflation", "total_inflation")

        self.expenses = total_inflation * self.manager.config["luxury_expenses"]
        if self.profile.luxury_level == 1:
            self.expenses *= 0.5
        if self.profile.luxury_level == 0:
            self.expenses = 0.5

        self.add_expenses(self.expenses)
