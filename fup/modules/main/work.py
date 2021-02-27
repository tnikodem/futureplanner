import random
from fup.core.module import Module


class Job(Module):
    def __init__(self, manager):
        super().__init__(manager)
        # Module props
        self.income = 0

        # Main properties
        self.salary_per_month = manager.config["start_income"] / 12
        self.expires = manager.config["birth_year"] + int(random.gauss(mu=67, sigma=2))
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

        if self.year >= self.expires:
            self.income = 0
            self.unemployed_months = 0
            return

        self.salary_per_month *= (inflation + random.gauss(mu=.005, sigma=0.001))

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

        #        print(self.unemployed_since)

        self.income = (12 - self.unemployed_months) * self.salary_per_month

        self.add_income(self.income)


class Annuity(Module):
    def __init__(self, manager):
        super().__init__(manager)
        self.income = 0
        self.entgeltpunkte = manager.config["start_entgeltpunkte"]
        self.durchschnittseinkommen = 38901  # 2019
        self.rentenwert = 33 * 12  # 2019

    def next_year(self):
        inflation = self.get_prop("main.environment.Inflation", "inflation")
        job_income = self.get_prop("main.work.Job", "income")
        job_expires = self.get_prop("main.work.Job", "expires")

        self.rentenwert *= inflation
        self.durchschnittseinkommen *= inflation
        if self.year < job_expires:
            new_entgeldpunkte = min(job_income / self.durchschnittseinkommen, 2.1)
            self.entgeltpunkte += new_entgeldpunkte
            self.income = 0
        else:
            # Germany Anuity Formula
            # R = E * Z * R * A

            # E: Entgeltpunkte
            # Gehalt / deutsches Durchschnittseinkommen (38.901 in 2019)
            # max 2.1 Punkte/Jahr

            # Z: Zugangsfaktor
            # Z = 1, jeden Monat früher in Rente = -0.003

            # R: Rentenart-Faktor
            # Altersrente: 1

            # A: Rentenwert
            # 33€ / Monat (2019)

            self.income = self.entgeltpunkte * self.rentenwert

        self.add_income(self.income)
