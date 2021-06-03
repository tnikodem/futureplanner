import numpy as np
import pandas as pd
from fup.core.module import ChangeModule


class Taxes(ChangeModule):
    def __init__(self, tax_rates, tax_offsets, taxable_incomes, name="", manager=None, **kwargs):
        super().__init__(name=name, manager=manager, **kwargs)
        self.tax_rates = pd.DataFrame(tax_rates)
        self.tax_offsets = tax_offsets
        self.taxable_incomes = taxable_incomes

        self.tax_rate = 0
        self.tax_offset = 0
        self.taxable_income = 0

    def next_year(self):
        inflation = self.get_prop("main.environment.Inflation", "inflation")
        self.tax_rates["taxable_income"] *= inflation

        self.tax_offset = 0
        self.taxable_income = 0
        for expense in self.tax_offsets:
            self.tax_offset += self.get_prop(expense, "expenses")
        for income in self.taxable_incomes:
            self.taxable_income += self.get_prop(income, "income")
        self.taxable_income -= self.tax_offset
        self.taxable_income = max(0, self.taxable_income)

        index_tax_max = np.searchsorted(self.tax_rates.taxable_income, self.taxable_income)
        index_tax_min = index_tax_max - 1

        if index_tax_min < 0:
            self.tax_rate = self.tax_rates.tax_rate[0]
        elif index_tax_max >= len(self.tax_rates):
            self.tax_rate = self.tax_rates.tax_rate[len(self.tax_rates) - 1]
        else:
            tax_rate_min = self.tax_rates.tax_rate[index_tax_min]
            taxable_income_min = self.tax_rates.taxable_income[index_tax_min]
            tax_rate_max = self.tax_rates.tax_rate[index_tax_max]
            taxable_income_max = self.tax_rates.taxable_income[index_tax_max]
            self.tax_rate = tax_rate_min + (self.taxable_income - taxable_income_min) / (
                    taxable_income_max - taxable_income_min) * (tax_rate_max - tax_rate_min)

        self.expenses = self.taxable_income * self.tax_rate

        self.df_row["tax"] = self.expenses
        self.df_row["tax_offset"] = self.tax_offset
