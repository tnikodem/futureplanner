import random
from fup.core.module import Module


class Taxes(Module):
    def __init__(self, manager):
        super().__init__(manager)
        self.tax = 0
        self.tax_rate = 0

        # freisteuer
        self.tax_free_limit = 10000  # in €
        self.max_tax_increase_limit = 100000  # in €
        self.min_tax_rate = 0.14
        self.max_tax_rate = 0.42 + random.gauss(mu=0, sigma=0.03)

    def add_info(self, info):
        info["tax"] = self.tax
        info["tax_rate"] = self.tax_rate

    def next_year(self):
        inflation = self.get_prop("main.environment.Inflation", "inflation")
        taxable_income = self.get_prop("main.work.Job", "income")

        self.tax_free_limit *= inflation
        self.max_tax_increase_limit *= inflation

        # calculate tax rate estimation
        if taxable_income < self.tax_free_limit:
            self.tax_rate = 0
        else:
            tax_increase = (self.max_tax_rate - self.min_tax_rate) / (self.max_tax_increase_limit - self.tax_free_limit)
            self.tax_rate = self.min_tax_rate + (taxable_income - self.tax_free_limit) * tax_increase
        self.tax_rate = min(self.tax_rate, self.max_tax_rate)

        self.tax = self.tax_rate * taxable_income

        self.add_expenses(self.tax)