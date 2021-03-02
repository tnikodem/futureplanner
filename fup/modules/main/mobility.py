from fup.core.module import Module


class Car(Module):
    def __init__(self, manager):
        super().__init__(manager)
        self.expenses = manager.config["car_expenses"]

    def next_year(self):
        total_inflation = self.get_prop("main.environment.Inflation", "total_inflation")
        if self.profile.luxury_level == 0:
            self.expenses = 0
        elif self.profile.luxury_level == 1:
            self.expenses = 0.5 * total_inflation * self.manager.config["car_expenses"]
        else:
            self.expenses = total_inflation * self.manager.config["car_expenses"]

        self.add_expenses(self.expenses)
