import random
from fup.core.module import ChangeModule


class Investing(ChangeModule):
#    def __init__(self, assets_stock_ratio, assets_gold_ratio):
#        self.assets_stock_ratio = assets_stock_ratio
#        self.assets_gold_ratio = assets_gold_ratio

    def next_year(self):
        self.expenses = 0
        total_assets = self.manager.total_assets

        stock_value = self.get_prop("assets.stocks.Stocks", "money_value")
        change_stock = self.get_prop("assets.stocks.Stocks", "change")

        gold_value = self.get_prop("assets.resources.Gold", "money_value")
        change_gold = self.get_prop("assets.resources.Gold", "change")

        change_money = self.get_prop("assets.money.Money", "change")

        # stocks
        stock_change = self.assets_stock_ratio * total_assets - stock_value
        change_money(money=change_stock(money=stock_change))

        # gold
        gold_change = self.assets_gold_ratio * total_assets - gold_value
        change_money(money=change_gold(money=gold_change))
