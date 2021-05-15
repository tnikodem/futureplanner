import collections
import copy


class Manager:
    def __init__(self, config, module_list, monitoring_class=None, profile_class=None):
        self.config = copy.deepcopy(config)
        self.year = config["simulation"]["start_year"]
        self.df_row = dict(year=self.year)

        # Modules
        # TODO put sorting of dependencies here?!  - you only want to do sorting once...
        self.modules = collections.OrderedDict()
        for module in module_list:
            self.add_module(module)

        # Monitoring to get summary for toy. Monitoring does NOT provide information for modules
        self.monitoring = None
        if monitoring_class:
            self.monitoring = monitoring_class(manager=self)

        # Profile to provide information for modules about current situation of life
        self.profile = None
        if profile_class:
            self.profile = profile_class(manager=self)

    def add_module(self, module):
        self.modules[module.name] = module.module_class(name=module.name, manager=self, **module.module_config)

    def get_module(self, module_name):
        return self.modules[module_name]

    def next_year(self):
        self.year += 1
        self.df_row = dict(year=self.year)
        for module_name in self.modules:
            self.modules[module_name].next_year_wrapper()
        if self.profile:
            self.profile.update()
        if self.monitoring:
            self.monitoring.next_year()

    def dependency_check(self):
        for module_name in self.modules:
            self.modules[module_name].dependency_check = True
            self.modules[module_name].next_year_wrapper()

    @property
    def total_assets(self):
        total_assets = 0
        for module_name in self.modules:
            if hasattr(self.modules[module_name], 'money_value'):
                total_assets += self.modules[module_name].money_value
        return total_assets
