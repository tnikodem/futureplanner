import random
from fup.core.module import ChangeModule


class Investing(ChangeModule):
    def next_year(self):
        total_assets = self.manager.total_assets
        change_money = self.manager.current_account.change

        for asset, ratio in self.assets_ratios.items():
            value = self.get_prop(asset, "money_value")
            change_asset = self.get_prop(asset, "change")
            delta = ratio * total_assets - value
            change_money(money=change_asset(money=delta))
