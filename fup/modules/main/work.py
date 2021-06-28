import random
from fup.core.module import ChangeModule


class Job(ChangeModule):
    """
    TODO How much does it costs/earn to find a new job?
    - Movement ?
    - Lower/higher salary ?
    - Compensation
    """

    def __init__(self, start_income, prob_find_job, prob_lose_job, unemployed_months=0,
                 salary_increase_mod=1, name="", manager=None, **kwargs):
        super().__init__(name=name, manager=manager, **kwargs)

        self.salary_per_month = start_income / 12
        self.salary_increase_mod = salary_increase_mod

        self.prob_find_job = prob_find_job
        self.prob_lose_job = prob_lose_job

        self.unemployed_months = unemployed_months
        self.unemployed_months_this_year = 0

    def get_age_salary_increase(self):
        """
        income increase https://www.stepstone.de/gehaltspotenzial-rechner
        years: gross income (average germany)
        22: 32,000
        50: 60,000
        65: 54,000

        IMPORTANT: such big increases are only possible by changing jobs!
        """
        age = self.manager.year - self.manager.profile.birth_year
        if age < 50:
            return 1.0227
        else:
            return 0.993

    def next_year(self):
        inflation = self.get_prop("main.environment.Inflation", "inflation")
        self.salary_per_month *= inflation * self.salary_increase_mod * self.get_age_salary_increase()

        if self.manager.profile.retired:
            self.unemployed_months_this_year = 0
            return

        if self.config["simulation"]["random"]:
            self.unemployed_months_this_year = 0
            for i in range(12):  # 12 months
                if self.unemployed_months > 0:
                    if random.random() < self.prob_find_job:
                        self.unemployed_months = 0
                    else:
                        self.unemployed_months += 1
                        self.unemployed_months_this_year += 1
                else:
                    if random.random() < self.prob_lose_job:
                        self.unemployed_months = 1
                        self.unemployed_months_this_year += 1

        self.income = (12 - self.unemployed_months_this_year) * self.salary_per_month
