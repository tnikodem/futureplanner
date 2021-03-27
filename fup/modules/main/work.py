import random
from fup.core.module import ChangeModule


class Job(ChangeModule):
    def __init__(self, manager):
        super().__init__(manager)
        # Module props
        self.income = 0

        # Main properties
        self.salary_per_month = manager.config["start_income"] / 12
        self.expires = manager.config["retirement_year"]
        self.birth_year = manager.config["birth_year"]

        # Helper props
        self.prob_lose_job = 1. / 90.
        self.prob_find_job = 1. / 12.
        # How much does it costs to find a new job?
        # Movement ?
        # Lower salary?
        # ... ?
        self.unemployed_since = 0
        self.unemployed_months = 0

    def next_year(self):
        # dependencies on the very top!
        inflation = self.get_prop("main.environment.Inflation", "inflation")

        #        if self.year - self.birth_year > 50:
        #            self.prob_lose_job = 1./60.   # ???
        #            self.prob_find_job = 1./120.  # ???

        if self.profile.retired:
            self.income = 0
            self.unemployed_months = 0
            return

        if self.config["random"]:
            self.salary_per_month *=  (inflation + random.gauss(mu=.005, sigma=0.001))
            self.unemployed_months = 0
            for i in range(12):  # 12 months
                if self.unemployed_since > 0:
                    if random.random() < self.prob_find_job:
                        self.unemployed_since = 0
                else:
                    if random.random() < self.prob_lose_job:
                        self.unemployed_since = 1

                if self.unemployed_since > 0:
                    self.unemployed_since += 1
                    self.unemployed_months += 1
        else:
            self.salary_per_month *= inflation

        self.income = (12 - self.unemployed_months) * self.salary_per_month

        self.add_income(self.income)