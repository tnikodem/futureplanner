from fup.core.module import ChangeModule


class InflationSensitive(ChangeModule):
    def next_year(self):
        total_inflation = self.get_prop("main.environment.Inflation", "total_inflation")
        self.expenses = self.start_expenses * total_inflation

    def add_info(self, info_dict):
        if hasattr(self, "info_name"):
            info_dict[self.info_name] = self.expenses


class InflationSensitiveVariable(ChangeModule):
    def next_year(self):
        total_inflation = self.get_prop("main.environment.Inflation", "total_inflation")
        self.expenses = self.start_expenses * total_inflation * (1. + self.manager.profile.money_level / 10.)

    def add_info(self, info_dict):
        if hasattr(self, "info_name"):
            info_dict[self.info_name] = self.expenses
