import collections
import copy


class Manager:
    def __init__(self, config, module_blueprints=None, profile_blueprint=None):
        self.config = copy.deepcopy(config)
        self.year = config["simulation"]["start_year"]
        self.modules = collections.OrderedDict()
        self.profile = None  # Profile to provide information for modules about current situation of life
        self.df_row = dict(year=self.year)

        if module_blueprints is not None:
            for module_blueprint in module_blueprints:  # TODO put sorting of dependencies here?!  - you only want to do sorting once...
                self.add_module(module_blueprint)
        if profile_blueprint is not None:
            self.add_profile(profile_blueprint)

    def add_module(self, module_blueprint):
        self.modules[module_blueprint.name] = module_blueprint.build_class(name=module_blueprint.name,
                                                                           manager=self,
                                                                           **module_blueprint.build_config)

    def add_profile(self, profile_blueprint):
        self.profile = profile_blueprint.build_class(manager=self, **profile_blueprint.build_config)

    def get_module(self, module_name):
        return self.modules[module_name]

    def next_year(self):
        self.year += 1
        self.df_row = dict(year=self.year)
        for module_name in self.modules:
            self.modules[module_name].next_year_wrapper()
        if self.profile:
            self.profile.update()

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
