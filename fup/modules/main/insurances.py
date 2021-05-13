from fup.core.module import ChangeModule


class InsuranceHealth(ChangeModule):
    def next_year(self):
        income = self.get_prop("main.work.Job", "income") + self.get_prop("main.insurances.InsurancePension", "income")
        self.expenses = income * self.fraction_of_income


class InsuranceNursingCare(ChangeModule):
    def next_year(self):
        income = self.get_prop("main.work.Job", "income") + self.get_prop("main.insurances.InsurancePension", "income")
        if self.manager.profile.retired:
            self.expenses = income * self.fraction_of_income * self.retirement_factor
        else:
            self.expenses = income * self.fraction_of_income


class InsurancePension(ChangeModule):
    @property
    def expected_income(self):
        # expect to have similar income until retirement
        job_income = self.get_prop("main.work.Job", "income")
        new_entgeldpunkte = min(job_income / self.durchschnittseinkommen, 2.1)
        years_till_retirement = max((self.config["profile"]["retirement_year"] - self.manager.year), 0)
        expected_entgeldpunkte = self.entgeltpunkte + years_till_retirement * new_entgeldpunkte
        return expected_entgeldpunkte * self.rentenwert

    def next_year(self):
        inflation = self.get_prop("main.environment.Inflation", "inflation")
        job_income = self.get_prop("main.work.Job", "income")

        self.rentenwert *= inflation
        self.durchschnittseinkommen *= inflation
        if not self.manager.profile.retired:
            self.new_entgeldpunkte = min(job_income / self.durchschnittseinkommen, 2.1)
            self.entgeltpunkte += self.new_entgeldpunkte
            self.income = 0
            self.expenses = self.fraction_of_income * job_income
        else:
            # Germany Pension Formula
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
            self.expenses = 0


class InsuranceUnemployment(ChangeModule):
    def next_year(self):
        birth_year = self.config["profile"]["birth_year"]
        job_income = self.get_prop("main.work.Job", "income")
        unemployed_months = self.get_prop("main.work.Job", "unemployed_months")
        unemployed_since = self.get_prop("main.work.Job", "unemployed_since")
        if self.manager.profile.retired:
            return

        # tax_rate = self.get_prop("main.taxes.Taxes", "tax_rate")
        salary_per_month = job_income / (12 - unemployed_months)
        months_you_get_unemployment_money = self.months_you_get_unemployment_money
        if self.manager.year - birth_year > 50:
            months_you_get_unemployment_money = 24

        self.expenses = job_income * self.fraction_of_income
        if unemployed_months > 0:

            month_you_get_money = unemployed_months
            if unemployed_since > months_you_get_unemployment_money:
                month_you_get_money -= (unemployed_since - months_you_get_unemployment_money)
            month_you_get_money = max(month_you_get_money, 0)

            # TODO better formula to get unemployment money, howver Prio B...
            self.income = month_you_get_money * salary_per_month * self.salary_fraction
