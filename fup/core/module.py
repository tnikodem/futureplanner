from fup.core.functions import get_full_name


class Module:
    def __init__(self, manager=None):
        self.manager = manager
        self.depends_on_modules = set()
        self.modifies_modules = set()
        self.expenses = 0
        self.income = 0

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
        self.manager.income += income

    def add_expenses(self, expenses):
        self.manager.expenses += expenses

    def next_year(self):
        pass

    def add_info(self, info_dict):
        pass

    def info_dict(self):
        return dict(
            name=get_full_name(self.__class__),
            income=self.income,
            expenses=self.expenses
        )

    def __repr__(self):
        return f"""{get_full_name(self.__class__)}: income: {self.income} expenses: {self.expenses}"""
