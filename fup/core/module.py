class Module:
    def __init__(self, manager=None):
        self.manager = manager
        self.depends_on_modules = set()
        self.modifies_modules = set()

    def set_manager(self, manager):
        self.manager = manager

    @property
    def year(self):
        return self.manager.year

    @property
    def config(self):
        return self.manager.config

    @property
    def profile(self):
        return self.manager.profile

    def get_prop_setter(self, module_name, prop):
        if module_name not in self.modifies_modules:
            self.modifies_modules.add(module_name)
        return lambda x: setattr(self.manager.get_module(module_name), prop, x)

    def get_prop(self, module, prop):
        if module not in self.depends_on_modules:
            self.depends_on_modules.add(module)
        return getattr(self.manager.get_module(module), prop)

    def add_income(self, income):
        self.manager.total_income += income

    def add_expenses(self, expenses):
        self.manager.total_expenses += expenses

    def next_year(self):
        pass

    def add_info(self, info):
        pass
