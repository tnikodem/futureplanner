class Monitoring:
    def __init__(self, manager):
        self.manager = manager

        self.unemployed_months = 0
        self.total_income = 0
        self.total_tax = 0

        self.years_luxury_level_0 = 0
        self.years_luxury_level_1 = 1
        self.years_luxury_level_2 = 2

    def next_year(self):
        self.unemployed_months += self.manager.get_module("main.work.Job").unemployed_months
        self.total_income += self.manager.total_income  # TODO tax corrected?!
        self.total_tax += self.manager.get_module("main.taxes.Taxes").expenses

        self.years_luxury_level_0 += self.manager.profile.luxury_level == 0
        self.years_luxury_level_1 += self.manager.profile.luxury_level == 1
        self.years_luxury_level_2 += self.manager.profile.luxury_level == 2

    def get_stats(self):
        return dict(unemployed_months=self.unemployed_months,
                    total_income=self.total_income,
                    total_tax=self.total_tax,
                    total_inflation=self.manager.get_module("main.environment.Inflation").total_inflation,
                    years_luxury_level_0=self.years_luxury_level_0,
                    years_luxury_level_1=self.years_luxury_level_1,
                    years_luxury_level_2=self.years_luxury_level_2,
                    )
