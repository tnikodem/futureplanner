from fup.core.functions import get_full_name

class Module:
    def __init__(self, manager=None):
        self.manager = manager
        self.depends_on_modules = set()
        self.modifies_modules = set()
        self.dependency_check = False
        self.reset_values = dict()

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

    # TODO rename set_prop and get_prop to show difference
    def set_prop(self, prop_name, value):
        if prop_name not in self.reset_values:
            self.reset_values[prop_name] = getattr(self, prop_name)
        if value is None:
            setattr(self, prop_name, self.reset_values[prop_name])
            del self.reset_values[prop_name]
        else:
            setattr(self, prop_name, value)

    def get_prop(self, module_name, prop_name):
        if self.dependency_check:
            self.depends_on_modules.add(module_name)
        return getattr(self.manager.get_module(module_name), prop_name)

    def get_prop_setter(self, module_name, prop_name):
        if self.dependency_check:
            self.modifies_modules.add(module_name)
        return lambda x: self.manager.get_module(module_name).set_prop(prop_name=prop_name, value=x)

    def get_prop_setter_function(self, module_name, prop):
        if self.dependency_check:
            self.modifies_modules.add(module_name)
        return getattr(self.manager.get_module(module_name), prop)

    # wrapper which can be overwritten by submodule class
    def calc_next_year(self):
        self.next_year()

    # Implemented by each module definition
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
        self._expenses = 0
        self._expense_modifier = 1
        self._income = 0
        self._income_modifier = 1

    @property
    def expenses(self):
        return self._expenses * self._expense_modifier

    @expenses.setter
    def expenses(self, value):
        self._expenses = value

    @property
    def income(self):
        return self._income * self._income_modifier

    @income.setter
    def income(self, value):
        self._income = value

    def calc_next_year(self):
        self.next_year()
        self.manager.income += self.income
        self.manager.expenses += self.expenses

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
        self.settlement_tax = 0
        self.exchange_fee = 0

    @property
    def money_value(self):
        return self.count * self.asset_value

    # TODO need unit test!!
    def change(self, money):
        if money > 0:
            self.add_asset_value = 1
            self.add_count = money / self.add_asset_value * (1-self.exchange_fee)
            self.asset_value = (self.count * self.add_asset_value + self.add_count *self.add_asset_value) / \
                               (self.count + self.add_count)
            self.count += self.add_count
            return -money
        else:
            self.count += money/self.asset_value
            return -money*(1-self.settlement_tax)*(1-self.exchange_fee)

    def change_value(self, relative_change):
        self.asset_value *= relative_change

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