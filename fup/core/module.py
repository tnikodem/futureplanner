from fup.core.functions import get_full_class_name


class Module:
    def __init__(self, name="", manager=None):
        self.name = name
        self.manager = manager
        self.depends_on_modules = set()
        self.modifies_modules = set()
        self.dependency_check = False
        self.reset_values = dict()

    @property
    def config(self):
        return self.manager.config

    def get_prop(self, module_name, prop_name):
        if self.dependency_check:
            self.depends_on_modules.add(module_name)
        return getattr(self.manager.get_module(module_name), prop_name)

    def change_prop(self, prop_name, change_value):
        prop_value = getattr(self, prop_name)
        prop_value *= change_value
        setattr(self, prop_name, prop_value)

    def get_prop_changer(self, module_name, prop_name):
        if self.dependency_check:
            self.modifies_modules.add(module_name)
        return lambda x: self.manager.get_module(module_name).change_prop(prop_name=prop_name, change_value=x)

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
        return {
            "name": self.name,
            "class": get_full_class_name(self.__class__),
            "info": self.get_extra_info()
        }

    def __repr__(self):
        return f"""{get_full_class_name(self.__class__)}"""


class ChangeModule(Module):
    def __init__(self, name="", manager=None):
        super().__init__(name=name, manager=manager)
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
        out_dict = super().info_dict()
        out_dict["income"] = self.income
        out_dict["expenses"] = self.expenses
        return out_dict

    def __repr__(self):
        return f"""{get_full_class_name(self.__class__)}: income: {int(self.income)}€ expenses: {int(self.expenses)}€"""


class AssetModule(Module):
    def __init__(self, name="", manager=None):
        super().__init__(name=name, manager=manager)
        self.count = 0
        self.asset_value = 1
        self.settlement_tax = 0
        self.exchange_fee = 0

    @property
    def money_value(self):
        return self.count * self.asset_value

    # TODO check and unit test!!
    def change(self, money):
        if money > 0:
            add_asset_value = 1
            add_count = money / add_asset_value * (1 - self.exchange_fee)
            self.asset_value = (self.count * self.asset_value + add_count * add_asset_value) / \
                               (self.count + add_count)
            self.count += add_count
            return -money
        else:
            return_money = abs(money)
            self.count -= return_money / self.asset_value
            if self.asset_value > 1:
                return_money -= return_money * (self.asset_value - 1) / self.asset_value * self.settlement_tax
            return_money *= (1 - self.exchange_fee)  # TODO before or after tax??!
            return return_money

    def change_value(self, relative_change):
        self.asset_value *= relative_change

    def info_dict(self):
        out_dict = super().info_dict()
        out_dict["value"] = self.money_value
        return out_dict

    def __repr__(self):
        return f"""{get_full_class_name(self.__class__)}: count: {self.income} value: {int(self.get_money_value())}€"""
