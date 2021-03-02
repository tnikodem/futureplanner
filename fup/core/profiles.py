class DefaultProfile:
    def __init__(self, manager, config):
        self.manager = manager
        self.config = config

        self.married = False
        self.partner = False
        self.children = 0

        self.luxury_level = 0  # 0,1,2   0: only necessary stuff, 1: saving 2: normal

        self.update()

    # update once per year, or if necessary more often
    def update(self):
        money = self.manager.money
        income = self.manager.total_income
        expenses = self.manager.total_expenses
        job_income = self.manager.get_module("main.work.Job").income
        total_inflation = self.manager.get_module("main.environment.Inflation").total_inflation
        tax = self.manager.get_module("main.taxes.Taxes").expenses

        if job_income > self.config["start_income"] * total_inflation and\
                money > self.config["start_money"] * total_inflation:
            self.luxury_level = 2
        elif job_income > 0 and money > (expenses-income) * 10:
            self.luxury_level = 2
        elif money > ((expenses-tax)-0.5*(income-tax)) * 5:
            self.luxury_level = 1
        else:
            self.luxury_level = 0
