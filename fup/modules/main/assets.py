import random
from fup.core.module import AssetModule, ChangeModule


class Money(AssetModule):
    def __init__(self, manager):
        super().__init__(manager)

        self.count = manager.config["start_money"]
        self.asset_value = 1

    def add_info(self, info_dict):
        info_dict["money"] = self.money_value


class Stocks(AssetModule):
    def __init__(self, manager):
        super().__init__(manager)

        self.count = manager.config["start_stocks"]
        self.asset_value = 1
        # S&P 500 since 1900
        self.value_increase_mean = 0.038690  # TODO this is only price, add dividend
        self.value_increase_std = 0.2

    def next_year(self):
        if self.config["random"]:
            self.asset_value *= 1 + random.gauss(mu=self.value_increase_mean, sigma=self.value_increase_std)
        else:
            self.asset_value *= 1 + self.value_increase_mean

    def add_info(self, info_dict):
        info_dict["stocks"] = self.money_value


class SavingPlan(AssetModule):
    # TODO add that money is immobile for 5+ years
    def __init__(self, manager):
        super().__init__(manager)

        self.count = manager.config["start_saving_plan"]
        self.asset_value = 1
        self.mean_count_increase = 1.001

    def next_year(self):
        self.count *= self.mean_count_increase


class Gold(AssetModule):
    def __init__(self, manager):
        super().__init__(manager)

        self.count = manager.config["start_gold"]
        # Gold price since since 1950
        self.value_increase_mean = 0.076029
        self.value_increase_std = 0.231742

    def next_year(self):
        if self.config["random"]:
            self.asset_value *= 1 + random.gauss(mu=self.value_increase_mean, sigma=self.value_increase_std)
        else:
            self.asset_value *= 1 + self.value_increase_mean

    def add_info(self, info_dict):
        info_dict["gold"] = self.money_value


class Investment(ChangeModule):
    def __init__(self, manager):
        super().__init__(manager)
        self.assets_stock_ratio = manager.config["assets_stock_ratio"]
        self.assets_gold_ratio = manager.config["assets_gold_ratio"]

    def next_year(self):
        self.expenses = 0
        total_assets = self.manager.total_assets

        stock_value = self.get_prop("main.assets.Stocks", "money_value")
        change_stock = self.get_prop_setter_function("main.assets.Stocks", "change")

        gold_value = self.get_prop("main.assets.Gold", "money_value")
        change_gold = self.get_prop_setter_function("main.assets.Gold", "change")

        change_money = self.get_prop_setter_function("main.assets.Money", "change")

        # stocks
        stock_change = self.assets_stock_ratio * total_assets - stock_value
        change_stock(money=stock_change)
        change_money(money=-stock_change)
        self.expenses += abs(stock_change) * 0.01  # exchange costs

        # gold
        gold_change = self.assets_gold_ratio * total_assets - gold_value
        change_gold(money=gold_change)
        change_money(money=-gold_change)
        self.expenses += abs(gold_change) * 0.10  # exchange costs

        self.add_expenses(self.expenses)
