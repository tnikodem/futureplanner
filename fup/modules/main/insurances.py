import random
from fup.core.module import Module


class InsuranceUnemployment(Module):
    def __init__(self, manager):
        super().__init__(manager)
        # Module props
        self.income = 0

        # Main properties
        self.salary_fraction = 0.6
        self.birth_year = manager.config["birth_year"]

        # Helper properties
        self.months_you_get_unemployment_money = 12

    def next_year(self):
        salary_per_month = self.get_prop("main.work.Job", "salary_per_month")
        unemployed_months = self.get_prop("main.work.Job", "unemployed_months")
        unemployed_since = self.get_prop("main.work.Job", "unemployed_since")
        annuity = self.get_prop("main.work.Annuity", "income")
        tax_rate = self.get_prop("main.taxes.Taxes", "tax_rate")

        if self.year - self.birth_year > 50:
            self.months_you_get_unemployment_money = 24

        if unemployed_months < 1 or annuity > 0:
            self.income = 0
        else:
            month_you_get_money = unemployed_months
            if unemployed_since - self.months_you_get_unemployment_money > 0:
                month_you_get_money -= (unemployed_since - self.months_you_get_unemployment_money)
            month_you_get_money = max(month_you_get_money, 0)

            self.income = month_you_get_money * salary_per_month * (1 - tax_rate) * self.salary_fraction

        self.add_income(self.income)
