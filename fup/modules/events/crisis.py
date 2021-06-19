from fup.core.module import EventModule


class OilCrisis1973(EventModule):
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

    def next_year(self):
        multiply_prob_lose_job = self.get_prop_multiplier("main.work.Job", "prob_lose_job")
        multiply_prob_find_job = self.get_prop_multiplier("main.work.Job", "prob_find_job")
        multiply_mean_inflation = self.get_prop_multiplier("main.environment.Inflation", "inflation_mean")
        multiply_gold_value = self.get_prop_multiplier("assets.resources.Gold", "asset_value")
        multiply_stocks_value = self.get_prop_multiplier("assets.stocks.Stocks", "asset_value")

        if self.crisis_year == 0:
            multiply_prob_lose_job(2)
            multiply_prob_find_job(0.5)
            multiply_mean_inflation(8.7 / 2.2)
        elif self.crisis_year == 1:
            multiply_mean_inflation(12.3 / 8.7)
            multiply_gold_value(770. / 400.)
            multiply_stocks_value(3181 / 6300)
        elif self.crisis_year == 2:
            multiply_mean_inflation(6.9 / 12.3)
            multiply_gold_value(660. / 770.)
            multiply_stocks_value(4100. / 3181.)
        elif self.crisis_year == 3:
            multiply_prob_lose_job(0.5)
            multiply_prob_find_job(2)
            multiply_mean_inflation(2.2 / 6.9)
        else:
            self.active = False


class LostDecadeJapan1991(EventModule):
    """
    https://en.wikipedia.org/wiki/Lost_Decade_(Japan)
    Stagnation: Asset price BUBBLE collapse
    "Window guidance" policy

    inflation
    https://www.statista.com/statistics/270095/inflation-rate-in-japan/
    1987: 0%
    1992: 3%
    1998: 0%
    2002: -1%
    2005: 0%

    real estate: TOD implement real estate
    https://upload.wikimedia.org/wikipedia/commons/3/36/Sum_japan.svg
    1987: 100
    1990: 200
    1992: 150
    1995: 120
    2000: 100
    2005: 80

    stocks NIKKEI 225 (only one country, MSCI WORLD rising!):
    https://upload.wikimedia.org/wikipedia/commons/d/d4/Harga_Saham_Nikkei_225.png
    1987: 20,000
    1990: 35,000 (+75%)
    1993: 18,000 (-49%)
    2005: 13,000 (-28%)  (total: -35%)

    gold:   TODO is this really related to the lost decade??!!
    https://www.macrotrends.net/1333/historical-gold-prices-100-year-chart
    1987: 1000
    2000: 400
    2005: 600
    """

    def next_year(self):
        add_mean_inflation = self.get_prop_adder("main.environment.Inflation", "inflation_mean")
        multiply_stocks = self.get_prop_multiplier("assets.stocks.Stocks", "asset_value")
        multiply_gold = self.get_prop_multiplier("assets.resources.Gold", "asset_value")

        # TODO better handling of module start values
        inflation_mean_start = self.manager.get_module("main.environment.Inflation").inflation_mean_start

        if self.crisis_year < 1:  # 1987, start
            add_mean_inflation(-inflation_mean_start)
            multiply_stocks(1.205)
            multiply_gold(0.9319)
        elif self.crisis_year < 3:  # 1990, bubble max
            add_mean_inflation(3./4.)
            multiply_stocks(1.205)
            multiply_gold(0.9319)
        elif self.crisis_year < 5:  # 1992, crash
            add_mean_inflation(3./4.)
            multiply_stocks(0.71)
            multiply_gold(0.9319)
        elif self.crisis_year < 13:  # 2000, low
            add_mean_inflation(-4./8.)
            multiply_stocks(0.975)
            multiply_gold(0.9319)
        elif self.crisis_year < 18:  # 2005, recovery
            add_mean_inflation(1/5.)
            multiply_stocks(0.975)
            multiply_gold(1.0845)
        else:  # reset
            add_mean_inflation(inflation_mean_start)
            self.active = False


class GlobalFinanceCrisis2008(EventModule):
    pass


class WorldFinanceCrisis1929(EventModule):
    pass
