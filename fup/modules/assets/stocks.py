import random
from fup.core.module import AssetModule


class Stocks(AssetModule):
#    def __init__(self, start_money_value, value_increase_mean, value_increase_std, gains_tax,
#                 exchange_fee, depot_costs):
#        self.count = start_money_value
#        self.value_increase_mean = value_increase_mean
#        self.value_increase_std = value_increase_std
#        self.gains_tax = gains_tax
#        self.exchange_fee = exchange_fee
#        self.depot_costs = depot_costs

    def next_year(self):
        if self.config["simulation"]["random"]:
            self.asset_value *= 1 + random.gauss(mu=self.value_increase_mean, sigma=self.value_increase_std)
        else:
            self.asset_value *= 1 + self.value_increase_mean
        self.change(money=-self.money_value * self.depot_costs)

    def add_info(self, info_dict):
        info_dict["stocks"] = self.money_value
        info_dict["stocks_value"] = self.asset_value