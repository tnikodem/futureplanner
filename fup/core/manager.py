import collections
from fup.core.functions import get_full_name
from fup.core.monitoring import Monitoring
from fup.core.profiles import DefaultProfile


class Manager:
    def __init__(self, config, module_list):
        self.config = config

        # Globals
        self.year = config["start_year"]
        self.money = config["start_money"]
        self.total_income = 0  # at the end of year  # TODO rename to income
        self.total_expenses = 0  # at the end of year

        # Modules
        self.modules = collections.OrderedDict()
        for module in module_list:
            self.add_module(module)

        # Monitoring to get summary for toy. Monitoring does NOT provide information for modules
        self.monitoring = Monitoring(manager=self)

        # Profile to provide information for modules about current situation of life
        self.profile = DefaultProfile(config=config, manager=self)

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

        self.profile.update()
        self.monitoring.next_year()

    def get_stats(self):
        return self.monitoring.get_stats()

    def get_df_row(self):
        df_info = dict(year=self.year,
                       income=self.total_income,
                       expenses=self.total_expenses,
                       money=self.money)

        for module in self.modules:
            self.get_module(module).add_info(df_info)
        return df_info

