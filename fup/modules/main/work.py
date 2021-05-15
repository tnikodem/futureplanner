import random
from fup.core.module import ChangeModule


class Job(ChangeModule):
    # TODO
    # income increase till age of ~50, then decline  https://www.stepstone.de/gehaltspotenzial-rechner
    # How much does it costs to find a new job?
    # - Movement ?
    # - Lower salary?

    def __init__(self, start_income, prob_find_job, prob_lose_job, unemployed_months,
                 name="", manager=None, **kwargs):
        super().__init__(name=name, manager=manager, **kwargs)

        self.salary_per_month = start_income / 12

        self.prob_find_job = prob_find_job
        self.prob_lose_job = prob_lose_job

        self.unemployed_months = unemployed_months
        self.unemployed_months_this_year = 0

    def next_year(self):
        inflation = self.get_prop("main.environment.Inflation", "inflation")
        self.salary_per_month *= inflation

        if self.manager.profile.retired:
            self.unemployed_months = 0
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
