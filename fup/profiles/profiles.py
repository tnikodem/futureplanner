class Test:
    def __init__(self, manager):
        self.manager = manager
        self.config = manager.config

        self.married = False
        self.partner = False
        self.children = 0
        self.retired = self.config["simulation"]["start_year"] >= self.config["profile"]["retirement_year"]
        self.money_level = 10

    def update(self):
        self.retired = self.manager.year >= self.config["profile"]["retirement_year"]

    def add_info(self, info_dict):
        pass


class Default:
    def __init__(self, manager, config):
        self.manager = manager
        self.config = config

        self.married = False  # TODO
        self.partner = False  # TODO
        self.children = 0  # TODO
        self.retired = config["simulation"]["start_year"] >= config["profile"]["retirement_year"]

        self.years_count = 0
        self.avg_working_expenses_wo_tax = config["simulation"]["start_expenses"]
        # self.income_last_year = config["start_income"]
        # self.expenses_last_year =

        # TODO get this by a test run
        self.retirement_factor = self.config["profile"][
            "retirement_factor"]  # try to achieve this amount of expensives once you are retired

        self.money_level = 0  # -10 to 10
        # -10: you are bancrupt, only bread and butter for you
        #   0: your income and expenses do fit
        #  10: you have much too much, buy sth

        # money level is calculated in an iterative approach.
        # depending on your expenses of last years it is tried
        # to match your future expenses such that an equal level is achieved

    def add_info(self, info_dict):
        pass

    # update once per year, or if necessary more often
    def update(self):
        # get values from modules
        money = self.manager.total_assets
        income = self.manager.income
        expenses = self.manager.expenses
        expected_pension = self.manager.get_module("main.insurances.InsurancePension").expected_income

        inflation = self.manager.get_module("main.environment.Inflation").mean_inflation / 100 + 1
        tax = self.manager.get_module("main.taxes.Taxes").expenses

        insurances = 0
        for module_name in self.manager.modules:
            if "main.insurances." not in module_name:
                continue
            insurances += self.manager.modules[module_name].expenses

        years_till_retirement = max(0, (self.config["profile"]["retirement_year"] - self.manager.year))
        years_in_retirenment = (self.config["simulation"]["end_year"] + 1 - max(self.manager.year,
                                                                                self.config["profile"][
                                                                                    "retirement_year"]))

        # everything is *inflation corrected* money

        # before retirement
        money_at_retirement = money
        for i in range(years_till_retirement):
            money_at_retirement /= inflation  # TODO also add interest
            money_at_retirement += income - expenses  # assume income and expenses stay the same until retirement

        # after retirement
        if self.retired:
            expenses_wo_tax = expenses - tax - insurances
        else:
            expenses_wo_tax = self.avg_working_expenses_wo_tax * self.retirement_factor

        # TODO how much tax and insurances must be paid in retirement ??!!
        insurancerate_retired = 0.9
        taxrate_retired = 0.89
        income_wo_tax = (expected_pension * insurancerate_retired) * taxrate_retired
        for i in range(years_in_retirenment):
            money_at_retirement /= inflation  # TODO also add interest
            money_at_retirement += income_wo_tax - expenses_wo_tax

        if money_at_retirement > self.config["profile"]["desired_money_buffer"] * 10:
            self.money_level += 5
        if money_at_retirement > self.config["profile"]["desired_money_buffer"] * 4:
            self.money_level += 3
        elif money_at_retirement > self.config["profile"]["desired_money_buffer"] * 2:
            self.money_level += 1
        elif money_at_retirement < -self.config["profile"]["desired_money_buffer"]:
            self.money_level -= 3
        elif money_at_retirement < self.config["profile"]["desired_money_buffer"]:
            self.money_level -= 1
        self.money_level = min(10, self.money_level)
        self.money_level = max(-10, self.money_level)

        # update history values
        self.avg_working_expenses_wo_tax *= inflation
        if not self.retired:
            self.avg_working_expenses_wo_tax = (self.avg_working_expenses_wo_tax * self.years_count + expenses - tax - insurances) / (self.years_count + 1)

        # set own values
        self.years_count += 1
        self.retired = self.manager.year >= self.config["profile"]["retirement_year"]
