import random
from fup.core.module import Module


class Inflation(Module):
    def __init__(self, mean_inflation):
        self.mean_inflation = mean_inflation
        self.inflation = 1
        self.total_inflation = 1

    def next_year(self):
        # job_income = self.get_module(Job).income

        # TODO scenario inflation, why is it high or low?! On what else does it depend?
        # https://www.laenderdaten.info/Europa/Deutschland/inflationsraten.php

        if self.config["simulation"]["random"]:
            self.inflation = 1 + random.gauss(mu=self.mean_inflation, sigma=1) / 100
        else:
            self.inflation = 1 + self.mean_inflation/100

        self.total_inflation *= self.inflation

    def get_extra_info(self):
        return f"inflation: {round((self.inflation-1)*100,2)}"

    def add_info(self, info_dict):
        info_dict["inflation"] = self.inflation
        info_dict["total_inflation"] = self.total_inflation
