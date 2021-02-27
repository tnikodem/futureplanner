import collections
from fup.core.functions import get_full_name


class Manager:
    def __init__(self, config, module_list):
        self.config = config

        self.year = config["start_year"]
        self.modules = collections.OrderedDict()
        for module in module_list:
            self.add_module(module)

        # Money
        self.total_income = 0
        self.total_expenses = 0
        self.money = config["start_money"]

        # TODO put into Monitoring
        self.short_of_money = False
        self.short_of_income = False
        self.bancrupt = False

    def add_module(self, module):
        self.modules[get_full_name(module)] = module(self)

    def get_module(self, module_name):
        return self.modules[module_name]

    def next_year(self):
        self.year += 1
        self.total_income = 0
        self.total_expenses = 0
        for module_name in self.modules:
            self.modules[module_name].next_year()

        self.money = self.money + self.total_income - self.total_expenses

        # TODO put this in the profiles
        if self.total_income < 30000:
            self.short_of_income = True
        if self.money < 10000:
            self.short_of_money = True
        if self.money < 0:
            self.bancrupt = True

    def get_df_row(self):
        df_info = dict(year=self.year,
                       income=self.total_income,
                       expenses=self.total_expenses,
                       money=self.money)

        for module in self.modules:
            self.get_module(module).add_info(df_info)
        return df_info

