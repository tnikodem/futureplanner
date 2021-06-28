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
            multiply_mean_inflation(1.087 / 1.022) #
        elif self.crisis_year == 1:
            multiply_mean_inflation(1.123 / 1.087) #
            multiply_gold_value(770. / 400.)
            multiply_stocks_value(3181 / 6300)
        elif self.crisis_year == 2:
            multiply_mean_inflation(1.069 / 1.123) #
            multiply_gold_value(660. / 770.)
            multiply_stocks_value(4100. / 3181.)
        elif self.crisis_year == 3:
            multiply_prob_lose_job(0.5)
            multiply_prob_find_job(2)
            multiply_mean_inflation(1.022 / 1.069) #
        else:
            self.active = False


class LostDecadeJapan1991(EventModule):
    """
    https://en.wikipedia.org/wiki/Lost_Decade_(Japan)
    Stagnation: Asset price BUBBLE + collapse
    "Window guidance" policy

    inflation
    https://www.statista.com/statistics/270095/inflation-rate-in-japan/
    1987: 0%
    1992: 3%
    1998: 0%
    2002: -1%
    2005: 0%

    real estate: TODO implement real estate
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
        multiply_mean_inflation = self.get_prop_multiplier("main.environment.Inflation", "inflation_mean")

        multiply_stocks = self.get_prop_multiplier("assets.stocks.Stocks", "asset_value")
        multiply_gold = self.get_prop_multiplier("assets.resources.Gold", "asset_value")

        # # TODO better handling of module start values
        inflation_mean_start = self.manager.get_module("main.environment.Inflation").inflation_mean_start

        if self.crisis_year < 1:  # 1987, start
            multiply_mean_inflation(1/inflation_mean_start)
            multiply_stocks(1.205)
            multiply_gold(0.9319)
        elif self.crisis_year < 3:  # 1990, bubble max
            multiply_mean_inflation(1.00741707178)  # 1.03**(1/4)
            multiply_stocks(1.205)
            multiply_gold(0.9319)
        elif self.crisis_year < 5:  # 1992, crash
            multiply_mean_inflation(1.00741707178)  # 1.03**(1/4)
            multiply_stocks(0.71)
            multiply_gold(0.9319)
        elif self.crisis_year < 13:  # 2000, low
            multiply_mean_inflation(0.99506)  # (0.99/1.03)**(1/8)
            multiply_stocks(0.975)
            multiply_gold(0.9319)
        elif self.crisis_year < 18:  # 2005, recovery
            multiply_mean_inflation(1.002)  # (1/0.99)**(1/5)
            multiply_stocks(0.975)
            multiply_gold(1.0845)
        else:  # reset
            multiply_mean_inflation(inflation_mean_start)
            self.active = False


class GreatRecession2007(EventModule):
    """
    https://en.wikipedia.org/wiki/Great_Recession
    Recession + Housing price BUBBLE

    real estate: TODO implement real estate
    https://de.wikipedia.org/wiki/Datei:Case-Shiller_National_Home_Price_Index.svg
    2004: 140
    2006: 190
    2007: 190
    2009: 130

    inflation:
    https://www.macrotrends.net/countries/USA/united-states/inflation-rate-cpi
    2009: -0.5%, otherwise normal
    2010: 1%

    unemployment:
    https://www.statista.com/statistics/193290/unemployment-rate-in-the-usa-since-1990/
    2009-2011: double

    stocks:
    https://www.lynxbroker.ch/boerse/boerse-kurse/etf/die-besten-etfs/msci-world-die-besten-etfs-auf-den-weltindex/
    2004: 1000
    2008: 1600
    2009: 800
    2010: 1200

    gold:
    https://www.macrotrends.net/1333/historical-gold-prices-100-year-chart
    2004: 600
    2010: 1500

    """

    def next_year(self):
        multiply_prob_lose_job = self.get_prop_multiplier("main.work.Job", "prob_lose_job")
        multiply_prob_find_job = self.get_prop_multiplier("main.work.Job", "prob_find_job")
        multiply_mean_inflation = self.get_prop_multiplier("main.environment.Inflation", "inflation_mean")
        # add_mean_inflation = self.get_prop_adder("main.environment.Inflation", "inflation_mean")
        multiply_stocks = self.get_prop_multiplier("assets.stocks.Stocks", "asset_value")
        multiply_gold = self.get_prop_multiplier("assets.resources.Gold", "asset_value")

        # TODO better handling of module start values
        inflation_mean_start = self.manager.get_module("main.environment.Inflation").inflation_mean_start

        # start 2005
        if self.crisis_year < 4:  # till 2008
            multiply_stocks(1.12468)
            multiply_gold(1.164)
        elif self.crisis_year == 4:  # 2009, crash
            multiply_prob_lose_job(2)
            multiply_prob_find_job(0.5)
            multiply_mean_inflation(0.995/inflation_mean_start)
            multiply_stocks(0.5)
            multiply_gold(1.164)
        elif self.crisis_year == 5:  # 2010
            multiply_mean_inflation(1.01/0.995)
            multiply_stocks(1.5)
            multiply_gold(1.164)
        else:  # reset
            multiply_prob_lose_job(0.5)
            multiply_prob_find_job(2)
            multiply_mean_inflation(inflation_mean_start/1.01)
            self.active = False


class GermanHyperinflation1914(EventModule):
    # TODO Test outcome: divided by inflation everything is the same
    # TODO what happened to retail?
    """
    https://de.wikipedia.org/wiki/Deutsche_Inflation_1914_bis_1923
    https://en.wikipedia.org/wiki/Hyperinflation_in_the_Weimar_Republic
    http://www.hartwig-w.de/hartwig/ekh/19Jh-Lebenshaltung/1900-leben.htm
    Hyperinflation

    Inflation:
    Paper money vs gold
    1914: 1
    1918: 2 (*2)
    1919: 4 (*2)
    1920: 10 (*2.5)
    1921: 30 (*3)
    1922: 200 (*6.66)
    1923: 10000 (*50)
    1924: 1,000,000,000,000 (*100000000)
    currency reform
        cash: 10,000,000,000 : 0.01
        inflation: * 1/ 10,000,000,000

    Stocks
    https://de.wikipedia.org/wiki/Deutsche_Inflation_1914_bis_1923#/media/Datei:Aktienindex_des_Statistischen_Reichsamtes_in_Papiermark.png
    1918: 100
    1920: 100
    1921: 200
    1922: 1000
    1923: 10000
    1924: 20,000,000,000,000

    Gold
    https://upload.wikimedia.org/wikipedia/commons/7/7e/Goldpreis_in_Papiermark.png
    1918: 100
    1919: 150
    1920: 1000
    1921: 1000
    1922: 3000
    1923: 120,000
    1924:  100,000,000,000,000

    work:
    https://www.was-war-wann.de/historische_werte/monatslohn.html
    unemployment rate is low
    wages:
    # 1914: 90
    # 1915: 91 (*1.01)
    # 1916: 103 (*1.13)
    # 1917: 119 (*1.15)
    1918: 122 (*1.025)
    1919: 127 (*1.04)
    1920: 132 (*1.04)
    1921: 136 (*1.03)
    1922: 137 (*1.01)
    1923: 120RM (*0.88 * 1,000,000,000,000)
    1924: 122RM (*1.02)
    """

    def next_year(self):
        multiply_salary_increase = self.get_prop_multiplier("main.work.Job", "salary_increase")
        multiply_mean_inflation = self.get_prop_multiplier("main.environment.Inflation", "inflation_mean")
        multiply_stocks = self.get_prop_multiplier("assets.stocks.Stocks", "asset_value")
        multiply_gold = self.get_prop_multiplier("assets.resources.Gold", "asset_value")
        multiply_current_account = self.get_prop_multiplier("CurrentAccount", "money_value")

        if self.crisis_year == 0:  # 1919
            multiply_mean_inflation(2/1.02)
            multiply_gold(150/100)
            multiply_salary_increase(1.04/2.)
        elif self.crisis_year == 1:  # 1920
            multiply_mean_inflation(2.5/2.)
            multiply_gold(1000/150)
            multiply_salary_increase(2./2.5)
        elif self.crisis_year == 2:  # 1921
            multiply_mean_inflation(3./2.5)
            multiply_stocks(2)
            multiply_salary_increase(2.5/3)
        elif self.crisis_year == 3:  # 1922
            multiply_mean_inflation(6.5/3.)
            multiply_gold(3)
            multiply_stocks(5)
            multiply_salary_increase(1.01/1.04*3./6.5)
        elif self.crisis_year == 4:  # 1923
            multiply_mean_inflation(50./6.5)
            multiply_gold(40)  # TODO gold had to be sold! if above limit of 10 gold mark
            multiply_stocks(10)
            multiply_salary_increase(0.88/1.01*6.5/50)
        elif self.crisis_year == 5:  # 1924
            multiply_mean_inflation(1e8/50)
            multiply_gold(10000000000/12)
            multiply_stocks(2000000000)
            multiply_salary_increase(1.02/0.88 * 50/1e8)
        elif self.crisis_year == 6:  # 1925 money reform
            multiply_mean_inflation(2e-20)  # hack factor 1/2 because missing first years 1914-1918
            multiply_gold(1e-12)
            multiply_stocks(1e-12)
            multiply_current_account(1e-12)
            multiply_salary_increase(1/1.02 * 1/2e-20)
        else:
            multiply_mean_inflation(0.5*1.02e12)
            multiply_salary_increase(2e-12)
            self.active = False
