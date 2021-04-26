from fup.core.module import ChangeModule


class Car(ChangeModule):
    def __init__(self, start_expenses):
        self.start_expenses = start_expenses

    def next_year(self):
        total_inflation = self.get_prop("main.environment.Inflation", "total_inflation")
        self.expenses = total_inflation * self.start_expenses
