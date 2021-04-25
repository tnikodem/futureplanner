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

    def __init__(self, manager, start_year):
        super().__init__(manager)
        self.start_year = start_year

    def next_year(self):
        set_prob_lose_job = self.get_prop_setter("main.work.Job", "prob_lose_job")
        set_prob_find_job = self.get_prop_setter("main.work.Job","prob_find_job")
        set_mean_inflation = self.get_prop_setter("main.environment.Inflation", "mean_inflation")
        change_gold_value = self.get_prop_setter_function("main.assets.Gold", "change_value")
        change_stocks_value = self.get_prop_setter_function("main.assets.Stocks", "change_value")

        if self.year == self.start_year:
            set_prob_lose_job(20)
            set_prob_find_job(5)
            set_mean_inflation(8.7)
        elif self.year == self.start_year+1:
            set_mean_inflation(12.3)
            change_gold_value(770./400.)
            change_stocks_value(3181/6300)
        elif self.year == self.start_year + 2:
            set_mean_inflation(6.9)
            change_gold_value(660./770.)
            change_stocks_value(4100./3181.)
        elif self.year == self.start_year + 3:
            set_mean_inflation(None)
            set_prob_lose_job(None)
            set_prob_find_job(None)
        else:
            pass

    def get_extra_info(self):
        return f"start: {self.start_year}"
