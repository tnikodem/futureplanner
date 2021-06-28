import random
from fup.core.module import ChangeModule


class Job(ChangeModule):
    # TODO
    # income increase till age of ~50, then decline  https://www.stepstone.de/gehaltspotenzial-rechner
    # How much does it costs to find a new job?
    # - Movement ?
    # - Lower salary?
    # - Compensation

    def __init__(self, start_income, prob_find_job, prob_lose_job, unemployed_months=0,
                 salary_increase=1, name="", manager=None, **kwargs):
        super().__init__(name=name, manager=manager, **kwargs)

        self.salary_per_month = start_income / 12
        self.salary_increase = salary_increase

        self.prob_find_job = prob_find_job
        self.prob_lose_job = prob_lose_job

        self.unemployed_months = unemployed_months
        self.unemployed_months_this_year = 0

    def next_year(self):
        inflation = self.get_prop("main.environment.Inflation", "inflation")
        self.salary_per_month *= self.salary_increase * inflation

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
