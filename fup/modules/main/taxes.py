from fup.core.module import ChangeModule


class Taxes(ChangeModule):
    def calcualte_tax(self, taxable_income, total_inflation):
        tax_free_limit = self.tax_free_limit * total_inflation
        max_tax_increase_limit = self.max_tax_increase_limit * total_inflation

        taxable_income -= tax_free_limit
        if taxable_income <= 0:
            return 0

        # TODO this is not linear, but a step function
        tax_increase = (self.max_tax_rate - self.min_tax_rate) / (max_tax_increase_limit - self.tax_free_limit)
        tax_rate = self.min_tax_rate + taxable_income * tax_increase
        tax_rate = min(tax_rate, self.max_tax_rate)

        return tax_rate * taxable_income

    def next_year(self):
        total_inflation = self.get_prop("main.environment.Inflation", "total_inflation")

        taxable_income = 0
        for income in self.taxable_incomes:
            taxable_income += self.get_prop(income, "income")
        for expense in self.tax_offsets:
            taxable_income -= self.get_prop(expense, "expenses")
        taxable_income = max(0, taxable_income)

        self.expenses = self.calcualte_tax(taxable_income=taxable_income, total_inflation=total_inflation)

        # job, pension
        # insurances = self.get_prop("main.insurances.InsuranceHealth", "expenses")
        # insurances += self.get_prop("main.insurances.InsuranceNursingCare", "expenses")
        # insurances += self.get_prop("main.insurances.InsurancePension", "expenses")
        # insurances += self.get_prop("main.insurances.InsuranceUnemployment", "expenses")

    def add_info(self, info_dict):
        info_dict["tax"] = self.expenses
