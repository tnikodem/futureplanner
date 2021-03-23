import random
from fup.core.module import AssetModule, ChangeModule


class Money(AssetModule):
    def __init__(self, manager):
        super().__init__(manager)

        self.count = manager.config["start_money"]
        self.asset_value = 1

    def add_info(self, info_dict):
        info_dict["money"] = self.money_value
        info_dict["estate"] = info_dict.get("estate", 0) + self.money_value


class Stocks(AssetModule):
    def __init__(self, manager):
        super().__init__(manager)

        self.count = manager.config["start_stocks"]
        self.asset_value = manager.config["start_stock_value"]
        self.mean_value_increase = 1.005

    def next_year(self):
        inflation = self.get_prop("main.environment.Inflation", "inflation")
        self.asset_value *= self.mean_value_increase * inflation

    def add_info(self, info_dict):
        info_dict["estate"] = info_dict.get("estate", 0) + self.money_value


class Investment(ChangeModule):
    def __init__(self, manager):
        super().__init__(manager)

    def next_year(self):
        income = self.get_prop("main.work.Job", "income")
        stock_money_value = self.get_prop("main.assets.Stocks", "money_value")
        invest_stock = self.get_prop("main.assets.Stocks", "invest")
        harvest_stock = self.get_prop("main.assets.Stocks", "harvest")

        if income > 0:
            # always 10% in stocks
            invest_stock(income * 0.1)
            self.expenses = income * 0.1
            self.income = 0
        else:
            harvest_fation = 1 / 20  # always assume still 20 years
            harvest_stock(harvest_fation * stock_money_value)
            self.income = harvest_fation * stock_money_value
            self.expenses = 0

        self.add_expenses(self.expenses)
        self.add_income(self.income)
