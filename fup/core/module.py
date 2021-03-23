from fup.core.functions import get_full_name

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

    def get_prop_setter(self, module_name, prop, ignore_dependencies=False):
        if not ignore_dependencies and module_name not in self.modifies_modules:
            self.modifies_modules.add(module_name)
        return lambda x: setattr(self.manager.get_module(module_name), prop, x)

    def get_prop(self, module_name, prop, ignore_dependencies=False):
        if not ignore_dependencies and module_name not in self.modifies_modules:
            self.depends_on_modules.add(module_name)
        return getattr(self.manager.get_module(module_name), prop)

    def next_year(self):
        pass

    def add_info(self, info_dict):
        pass

    def get_extra_info(self):
        return ""

    def info_dict(self):
        return dict(
            name=get_full_name(self.__class__),
            income=0,
            expenses=0,
            value=0,
            info=self.get_extra_info()
        )

    def __repr__(self):
        return f"""{get_full_name(self.__class__)}"""


class ChangeModule(Module):
    def __init__(self, manager=None):
        super().__init__(manager)
        self.expenses = 0
        self.income = 0

    def add_income(self, income):
        self.manager.income += income

    def add_expenses(self, expenses):
        self.manager.expenses += expenses

    def info_dict(self):
        return dict(
            name=get_full_name(self.__class__),
            income=self.income,
            expenses=self.expenses,
            value=0,
            info=self.get_extra_info()
        )

    def __repr__(self):
        return f"""{get_full_name(self.__class__)}: income: {int(self.income)}€ expenses: {int(self.expenses)}€"""


class AssetModule(Module):
    def __init__(self, manager=None):
        super().__init__(manager)
        self.count = 0
        self.asset_value = 1

    @property
    def money_value(self):
        return self.count * self.asset_value

    def harvest(self, money):
        self.count -= money/self.asset_value

    def invest(self, money):
        self.count += money/self.asset_value

    def info_dict(self):
        return dict(
            name=get_full_name(self.__class__),
            income=0,
            expenses=0,
            value=self.money_value,
            info=self.get_extra_info()
        )

    def __repr__(self):
        return f"""{get_full_name(self.__class__)}: count: {self.income} value: {int(self.get_money_value())}€"""