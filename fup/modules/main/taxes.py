import random
from fup.core.module import ChangeModule


class Taxes(ChangeModule):
    def __init__(self, manager):
        super().__init__(manager)
        self.expenses = 0
        self.tax_rate = 0

        # freisteuer
        self.tax_free_limit = 10000  # in €
        self.max_tax_increase_limit = 100000  # in €
        self.min_tax_rate = 0.14
        self.max_tax_rate = 0.42  # + random.gauss(mu=0, sigma=0.03)

        self.real_tax_factor = 1

        # adjust tax based on current tax
        if self.config.get("start_taxable_income"):
            estimated_taxrate = self.calcualte_taxrate(taxable_income=self.config["start_taxable_income"])
            if estimated_taxrate > 0:
                self.real_tax_factor = 1.0 * self.config["start_tax"] / self.config["start_taxable_income"] / estimated_taxrate

    def calcualte_taxrate(self, taxable_income):
        # calculate tax rate estimation
        if taxable_income < self.tax_free_limit:
            self.tax_rate = 0
        else:
            tax_increase = (self.max_tax_rate - self.min_tax_rate) / (self.max_tax_increase_limit - self.tax_free_limit)
            self.tax_rate = self.min_tax_rate + (taxable_income - self.tax_free_limit) * tax_increase
        self.tax_rate = min(self.tax_rate, self.max_tax_rate)

        self.tax_rate *= self.real_tax_factor

        return self.tax_rate

    def next_year(self):
        inflation = self.get_prop("main.environment.Inflation", "inflation")

        income = self.get_prop("main.work.Job", "income")
        income += self.get_prop("main.insurances.InsurancePension", "income")

        insurances = self.get_prop("main.insurances.InsuranceHealth", "expenses")
        insurances += self.get_prop("main.insurances.InsuranceNursingCare", "expenses")
        insurances += self.get_prop("main.insurances.InsurancePension", "expenses")
        insurances += self.get_prop("main.insurances.InsuranceUnemployment", "expenses")

        taxable_income = income - insurances

        self.tax_free_limit *= inflation
        self.max_tax_increase_limit *= inflation

        self.tax_rate = self.calcualte_taxrate(taxable_income=taxable_income)
        self.expenses = taxable_income * self.tax_rate
