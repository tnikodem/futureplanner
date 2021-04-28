import random
from fup.core.module import ChangeModule


class OilCrisis1973(ChangeModule):
    """
    https://en.wikipedia.org/wiki/1973_oil_crisis
    Stagflation
    Oil price went from 20$ to 100$
    Many insolvencies, high unemployment -> economic groth went down
    Fiscal stimulus -> inflation

    Inflation 8.7 (1973) ->  12.3 (1974) -> 6.9 (1975)  https://www.macrotrends.net/2497/historical-inflation-rate-by-year
    Dow Jones 6300 (1973) -> 3181 (1974) -> 4100 (1975) https://www.macrotrends.net/1319/dow-jones-100-year-historical-chart
    Gold 400 (1973) -> 770 (1974) -> 660 (1975) https://www.macrotrends.net/1333/historical-gold-prices-100-year-chart
    >> Gold was legalised 1973 in USA!
    """

    def __init__(self, start_year=None, probability=None):
        self.start_year = start_year
        self.probability = probability
        self.active = False

    def next_year(self):
        change_prob_lose_job = self.get_prop_changer("main.work.Job", "prob_lose_job")
        change_prob_find_job = self.get_prop_changer("main.work.Job","prob_find_job")
        change_mean_inflation = self.get_prop_changer("main.environment.Inflation", "mean_inflation")
        change_gold_value = self.get_prop_changer("main.assets.Gold", "asset_value")
        change_stocks_value = self.get_prop_changer("main.assets.Stocks", "asset_value")

        if self.probability and not self.active:
            if self.config["simulation"]["random"]:
                if random.random() < self.probability:
                    self.start_year = self.manager.year

        if self.start_year:
            if self.manager.year == self.start_year:
                self.active = True
                change_prob_lose_job(2)
                change_prob_find_job(0.5)
                change_mean_inflation(8.7/2.2)
            elif self.manager.year == self.start_year+1:
                self.active = True
                change_mean_inflation(12.3/8.7)
                change_gold_value(770./400.)
                change_stocks_value(3181/6300)
            elif self.manager.year == self.start_year + 2:
                self.active = True
                change_mean_inflation(6.9/12.3)
                change_gold_value(660./770.)
                change_stocks_value(4100./3181.)
            elif self.manager.year == self.start_year + 3:
                self.active = True
                change_prob_lose_job(0.5)
                change_prob_find_job(2)
                change_mean_inflation(2.2/6.9)
            else:
                self.active = False

    def get_extra_info(self):
        return f"start: {self.start_year}"

    def add_info(self, info_dict):
        if self.active:
            if "crisis" in info_dict:
                info_dict["crisis"] += ","+self.name
            else:
                info_dict["crisis"] = self.name
