from fup.core.module import ChangeModule


class OtherExpenses(ChangeModule):
    def __init__(self, manager, start_expenses):
        super().__init__(manager)
        self.start_expenses = start_expenses

    def next_year(self):
        total_inflation = self.get_prop("main.environment.Inflation", "total_inflation")
        self.expenses = total_inflation * self.start_expenses
        self.add_expenses(self.expenses)


class LuxuryExpenses(ChangeModule):
    def __init__(self, manager, start_expenses):
        super().__init__(manager)
        self.start_expenses = start_expenses

    def next_year(self):
        total_inflation = self.get_prop("main.environment.Inflation", "total_inflation")

        self.expenses = total_inflation * self.start_expenses
        # adapt to money situation
        self.expenses *= 1. + self.profile.money_level/10.
        self.add_expenses(self.expenses)
