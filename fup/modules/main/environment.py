import random
from fup.core.module import Module


class Inflation(Module):
    def __init__(self, name="", manager=None, inflation_mean=2, inflation_std=1, **kwargs):
        super().__init__(name=name, manager=manager, **kwargs)
        self.inflation_mean = inflation_mean
        self.inflation_std = inflation_std
        self.inflation = 1
        self.total_inflation = 1

    def next_year(self):
        if self.config["simulation"]["random"]:
            self.inflation = 1 + random.gauss(mu=self.inflation_mean, sigma=self.inflation_std) / 100
        else:
            self.inflation = 1 + self.inflation_mean / 100
        self.total_inflation *= self.inflation

    def get_extra_info(self):
        return f"inflation: {round((self.inflation - 1) * 100, 2)}"

    def add_info(self, info_dict):
        info_dict["inflation"] = self.inflation
        info_dict["total_inflation"] = self.total_inflation
