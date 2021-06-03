from fup.core.functions import get_full_class_name
from fup.core.module import Module


class CurrentAccount(Module):
    def __init__(self,
                 start_money_value,
                 penalty_interest_limit=50000,
                 penalty_interest_rate=0.05,
                 overdraft_rate=0.0775,
                 name="", manager=None, **kwargs):
        super().__init__(name=name, manager=manager, **kwargs)

        self.money_value = start_money_value
        self.penalty_interest_limit = penalty_interest_limit
        self.penalty_interest_rate = penalty_interest_rate
        self.overdraft_rate = overdraft_rate

    @property
    def info(self):
        out_dict = super().info
        out_dict["value"] = self.money_value
        return out_dict

    def change(self, money):
        self.money_value += money
        return -money

    def next_year_wrapper(self):
        self.next_year()
        self.df_row["assets"] = self.df_row.get("assets", 0) + self.money_value

    def __repr__(self):
        return f"""{get_full_class_name(self.__class__)}: {int(self.money_value)}€"""

    def next_year(self):
        # TODO add calculations

        self.df_row["money"] = self.money_value
