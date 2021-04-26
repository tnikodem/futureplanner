import random
from fup.core.module import ChangeModule


class InsuranceHealth(ChangeModule):
    def __init__(self, fraction_of_income=0.073 ):
        self.fraction_of_income = fraction_of_income
    def next_year(self):
        income = self.get_prop("main.work.Job", "income") + self.get_prop("main.insurances.InsurancePension", "income")
        self.expenses = income * self.fraction_of_income


class InsuranceNursingCare(ChangeModule):
    def __init__(self, fraction_of_income=0.0165):
        self.fraction_of_income = fraction_of_income

    def next_year(self):
        income = self.get_prop("main.work.Job", "income") + self.get_prop("main.insurances.InsurancePension", "income")
        fraction_of_income = self.fraction_of_income
        if self.profile.retired:
            fraction_of_income *= 2
        self.expenses = income * self.fraction_of_income


class InsurancePension(ChangeModule):
    def __init__(self, start_entgeltpunkte):
        self.entgeltpunkte = start_entgeltpunkte
        self.new_entgeldpunkte = 0
        self.durchschnittseinkommen = 38901  # 2019
        self.rentenwert = 33 * 12  # 2019
        self.fraction_of_income = 0.186 * 0.5

    @property
    def expected_income(self):
        years_till_retirement = max((self.config["profile"]["retirement_year"] - self.year), 0)
        expected_entgeldpunkte = self.entgeltpunkte + years_till_retirement * self.new_entgeldpunkte
        return expected_entgeldpunkte * self.rentenwert

    def next_year(self):
        inflation = self.get_prop("main.environment.Inflation", "inflation")
        job_income = self.get_prop("main.work.Job", "income")

        self.rentenwert *= inflation
        self.durchschnittseinkommen *= inflation
        if not self.profile.retired:
            self.new_entgeldpunkte = min(job_income / self.durchschnittseinkommen, 2.1)
            self.entgeltpunkte += self.new_entgeldpunkte
            self.income = 0
            self.expenses = self.fraction_of_income * job_income
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
            self.expenses = 0



class InsuranceUnemployment(ChangeModule):
    def __init__(self):
        # Main properties
        self.salary_fraction = 0.6
        # Helper properties
        self.months_you_get_unemployment_money = 12
        self.fraction_of_income = 0.024 * 0.5

    def next_year(self):
        birth_year = self.config["profile"]["birth_year"]
        salary_per_month = self.get_prop("main.work.Job", "salary_per_month")
        unemployed_months = self.get_prop("main.work.Job", "unemployed_months")
        unemployed_since = self.get_prop("main.work.Job", "unemployed_since")
        #tax_rate = self.get_prop("main.taxes.Taxes", "tax_rate")
        tax_rate = 0.3  # TODO better formula to get unemployment money, howver Prio B...

        if self.year - birth_year > 50:
            self.months_you_get_unemployment_money = 24

        if self.profile.retired:
            self.income = 0
            self.expenses = 0
        elif unemployed_months < 1:
            self.expenses = max(12-unemployed_months, 0) * salary_per_month * self.fraction_of_income
        else:
            month_you_get_money = unemployed_months
            if unemployed_since - self.months_you_get_unemployment_money > 0:
                month_you_get_money -= (unemployed_since - self.months_you_get_unemployment_money)
            month_you_get_money = max(month_you_get_money, 0)

            self.income = month_you_get_money * salary_per_month * (1 - tax_rate) * self.salary_fraction
            self.expenses = min(12-unemployed_months, 0) * salary_per_month * self.fraction_of_income
