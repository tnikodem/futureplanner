import collections
from fup.core.functions import get_full_class_name
from fup.core.monitoring import Monitoring
from fup.core.profiles import DefaultProfile

class ModuleConfig:
    def __init__(self, name, module_config, module_class):
        self.name = name
        self.module_config = module_config
        self.module_class = module_class

class Manager:
    def __init__(self, config, module_list, monitoring_class=None, profile_class=None):
        self.config = config

        # Globals
        self.year = config["simulation"]["start_year"]
        self.income = config["simulation"]["start_income"]
        self.expenses = config["simulation"]["start_expenses"]

        # Modules
        self.modules = collections.OrderedDict()
        for module in module_list:
            self.add_module(module)

        # Monitoring to get summary for toy. Monitoring does NOT provide information for modules
        if monitoring_class:
            self.monitoring = monitoring_class(manager=self)
        else:
            self.monitoring = Monitoring(manager=self)

        # Profile to provide information for modules about current situation of life
        if profile_class:
            self.profile = profile_class(config=config, manager=self)
        else:
            self.profile = DefaultProfile(config=config, manager=self)

    def add_module(self, module):
        self.modules[module.name] = module.module_class(**module.module_config)
        super(module.module_class, self.modules[module.name]).__init__(name=module.name, manager=self)
        self.modules[module.name].__init__(**module.module_config)  # TODO bit hacky??!

    def get_module(self, module_name):
        return self.modules[module_name]

    def next_year(self):
        self.year += 1
        self.income = 0
        self.expenses = 0
        for module_name in self.modules:
            self.modules[module_name].calc_next_year()

        self.get_module("main.assets.Money").count += self.income - self.expenses

        self.profile.update()
        self.monitoring.next_year()

    def dependency_check(self):
        for module_name in self.modules:
            self.modules[module_name].dependency_check = True
            self.modules[module_name].next_year()

    @property
    def total_assets(self):
        total_assets = 0
        for module_name in self.modules:
            if hasattr(self.modules[module_name], 'money_value'):
                total_assets += self.modules[module_name].money_value
        return total_assets

    def get_stats(self):
        return self.monitoring.get_final_stats()

    def get_df_row(self):
        info_dict = dict(year=self.year,
                         income=self.income,
                         expenses=self.expenses)
        for module in self.modules:
            self.get_module(module).add_info(info_dict)
        self.profile.add_info(info_dict)
        self.monitoring.add_info(info_dict)

        return info_dict



