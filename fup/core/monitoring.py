class Monitoring:
    def __init__(self, manager):
        self.manager = manager

        self.unemployed_months = 0
        self.money_levels_below_m3 = 0
        self.money_levels_above_3 = 1

    def next_year(self):
        self.unemployed_months += self.manager.get_module("main.work.Job").unemployed_months_this_year

        if self.manager.profile.money_level > 3:
            self.money_levels_above_3 += 1

        if self.manager.profile.money_level < -3:
            self.money_levels_below_m3 += 1

    def add_info(self, info_dict):
        info_dict["retired"] = self.manager.profile.retired
        info_dict["money_level"] = self.manager.profile.money_level
        info_dict["assets"] = self.manager.total_assets

    def get_final_stats(self):
        return dict(unemployed_months=self.unemployed_months,
                    total_inflation=self.manager.get_module("main.environment.Inflation").total_inflation,
                    money_levels_below_3=self.money_levels_below_m3,
                    money_levels_above_3=self.money_levels_above_3,
                    )
