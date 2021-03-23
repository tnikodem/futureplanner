from fup.core.module import ChangeModule


class OtherExpenses(ChangeModule):
    def __init__(self, manager):
        super().__init__(manager)
        self.expenses = manager.config["other_expenses"]

    def next_year(self):
        total_inflation = self.get_prop("main.environment.Inflation", "total_inflation")
        self.expenses = total_inflation * self.manager.config["other_expenses"]
        self.add_expenses(self.expenses)


class LuxuryExpenses(ChangeModule):
    def __init__(self, manager):
        super().__init__(manager)
        self.expenses = manager.config["other_expenses"]

    def next_year(self):
        total_inflation = self.get_prop("main.environment.Inflation", "total_inflation")

        self.expenses = total_inflation * self.manager.config["luxury_expenses"]
        # adapt to money situation
        self.expenses *= 1. + self.profile.money_level/10.
        self.add_expenses(self.expenses)
