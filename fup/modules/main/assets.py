import random
from fup.core.module import AssetModule, ChangeModule


class Money(AssetModule):
    def __init__(self, manager, start_money_value):
        super().__init__(manager)

        self.asset_value = 1
        self.change(money=start_money_value)

    def add_info(self, info_dict):
        info_dict["money"] = self.money_value


class Stocks(AssetModule):
    def __init__(self, manager, start_money_value, value_increase_mean, value_increase_std, settlement_tax,
                 exchange_fee, depot_costs):
        super().__init__(manager)
        self.count = start_money_value
        self.value_increase_mean = value_increase_mean
        self.value_increase_std = value_increase_std
        self.settlement_tax = settlement_tax
        self.exchange_fee = exchange_fee
        self.depot_costs = depot_costs

    def next_year(self):
        if self.config["simulation"]["random"]:
            self.asset_value *= 1 + random.gauss(mu=self.value_increase_mean, sigma=self.value_increase_std)
        else:
            self.asset_value *= 1 + self.value_increase_mean
        self.change(money=-self.money_value*self.depot_costs)

    def add_info(self, info_dict):
        info_dict["stocks"] = self.money_value


class Gold(AssetModule):
    def __init__(self, manager, start_money_value, value_increase_mean, value_increase_std, settlement_tax,
                 exchange_fee, depot_costs):
        super().__init__(manager)
        self.count = start_money_value
        self.value_increase_mean = value_increase_mean
        self.value_increase_std = value_increase_std
        self.settlement_tax = settlement_tax
        self.exchange_fee = exchange_fee
        self.depot_costs = depot_costs

    def next_year(self):
        if self.config["simulation"]["random"]:
            self.asset_value *= 1 + random.gauss(mu=self.value_increase_mean, sigma=self.value_increase_std)
        else:
            self.asset_value *= 1 + self.value_increase_mean
        self.change(money=-self.money_value*self.depot_costs)

    def add_info(self, info_dict):
        info_dict["gold"] = self.money_value


class Investment(ChangeModule):
    def __init__(self, manager, assets_stock_ratio, assets_gold_ratio):
        super().__init__(manager)
        self.assets_stock_ratio = assets_stock_ratio
        self.assets_gold_ratio = assets_gold_ratio

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
        change_money(money=change_stock(money=stock_change))

        # gold
        gold_change = self.assets_gold_ratio * total_assets - gold_value
        change_money(money=change_gold(money=gold_change))
