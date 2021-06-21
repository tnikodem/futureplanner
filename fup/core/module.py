import random
from fup.core.functions import get_full_class_name


class Module:
    def __init__(self, name="", manager=None, run_end_of_year=False, **kwargs):
        self.name = name
        self.manager = manager
        self.depends_on_modules = set()
        self.modifies_modules = set()
        self.dependency_check = False
        self.run_end_of_year = run_end_of_year

        for k, v in kwargs.items():
            assert isinstance(k, str)
            setattr(self, k, v)

    @property
    def config(self):
        return self.manager.config

    @property
    def df_row(self):
        return self.manager.df_row

    @property
    def info(self):
        return {
            "name": self.name,
            "class": get_full_class_name(self.__class__),
            "info": self.get_extra_info()
        }

    def get_prop(self, module_name, prop_name):
        if self.dependency_check:
            self.depends_on_modules.add(module_name)
        return getattr(self.manager.get_module(module_name), prop_name)

    def add_prop(self, prop_name, change_value):
        prop_value = getattr(self, prop_name)
        setattr(self, prop_name, prop_value+change_value)

    def multiply_prop(self, prop_name, change_value):
        prop_value = getattr(self, prop_name)
        setattr(self, prop_name, prop_value*change_value)

    def get_prop_adder(self, module_name, prop_name):
        if self.dependency_check:
            self.modifies_modules.add(module_name)
        return lambda x: self.manager.get_module(module_name).add_prop(prop_name=prop_name, change_value=x)

    def get_prop_multiplier(self, module_name, prop_name):
        if self.dependency_check:
            self.modifies_modules.add(module_name)
        return lambda x: self.manager.get_module(module_name).multiply_prop(prop_name=prop_name, change_value=x)

    # wrapper which can be overwritten by submodule class
    def next_year_wrapper(self):
        self.next_year()

    # Implemented by each module definition
    def next_year(self):
        pass

    def get_extra_info(self):
        return ""

    def __repr__(self):
        return f"""{get_full_class_name(self.__class__)}"""


class AssetModule(Module):
    def __init__(self, name="", manager=None, start_money_value=0, gains_tax=0, exchange_fee=0, **kwargs):
        super().__init__(name=name, manager=manager, **kwargs)
        self.count = start_money_value
        self.asset_value = 1
        self.gains_tax = gains_tax
        self.exchange_fee = exchange_fee

    @property
    def money_value(self):
        return self.count * self.asset_value

    @property
    def info(self):
        out_dict = super().info
        out_dict["value"] = self.money_value
        return out_dict

    def change(self, money):
        if money > 0:
            add_money_value = money * (1 - self.exchange_fee)
            self.asset_value = (self.count * self.asset_value + add_money_value) / (self.count + add_money_value)
            self.count += add_money_value
            return -money
        else:
            asset_count = abs(money) / self.asset_value
            self.count -= asset_count
            asset_value_with_fee = self.asset_value * (1 - self.exchange_fee)
            return_money = asset_value_with_fee * asset_count
            if asset_value_with_fee > 1:
                return_money *= 1 - (asset_value_with_fee - 1) / asset_value_with_fee * self.gains_tax
            return return_money

    def change_value(self, relative_change):
        self.asset_value *= relative_change

    def next_year_wrapper(self):
        self.next_year()
        self.df_row["assets"] = self.df_row.get("assets", 0) + self.money_value

    def __repr__(self):
        return f"""{get_full_class_name(self.__class__)}: {int(self.money_value)}€"""


class EventModule(Module):
    def __init__(self, name="", manager=None, start_year=None, probability=None, **kwargs):
        super().__init__(name=name, manager=manager, **kwargs)
        self.start_year = start_year
        self.probability = probability
        self.active = False
        self.crisis_year = 0

    def get_extra_info(self):
        return f"start: {self.start_year}"

    def next_year_wrapper(self):
        if not self.dependency_check:
            if self.probability and not self.active:
                if self.config["simulation"]["random"]:
                    if random.random() < self.probability:
                        self.start_year = self.manager.year

            if self.start_year == self.manager.year:
                self.active = True

            if not self.active:
                return

            self.crisis_year = self.manager.year - self.start_year

        self.next_year()

        if self.active:
            if "event" in self.df_row:
                self.df_row["event"] += "," + self.name
            else:
                self.df_row["event"] = self.name

    def __repr__(self):
        return f"{get_full_class_name(self.__class__)}: active: {int(self.active)} start: {self.start_year}" \
               f" prob: {self.probability}"


class ChangeModule(Module):
    def __init__(self, name="", manager=None, **kwargs):
        super().__init__(name=name, manager=manager, **kwargs)
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

    @property
    def info(self):
        out_dict = super().info
        out_dict["income"] = self.income
        out_dict["expenses"] = self.expenses
        return out_dict

    def next_year_wrapper(self):
        self.income = 0
        self.expenses = 0

        self.next_year()
        self.manager.current_account.change(self.income - self.expenses)

        self.df_row["income"] = self.df_row.get("income", 0) + self.income
        self.df_row["expenses"] = self.df_row.get("expenses", 0) + self.expenses

    def __repr__(self):
        return f"""{get_full_class_name(self.__class__)}: income: {int(self.income)}€ expenses: {int(self.expenses)}€"""
