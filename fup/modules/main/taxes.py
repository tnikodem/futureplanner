from fup.core.module import ChangeModule


class Taxes(ChangeModule):
    def __init__(self, tax_free_limit, max_tax_increase_limit, min_tax_rate, max_tax_rate,
                 tax_offsets, taxable_incomes, name="", manager=None, **kwargs):
        super().__init__(name=name, manager=manager, **kwargs)
        self.tax_free_limit = tax_free_limit
        self.max_tax_increase_limit = max_tax_increase_limit
        self.min_tax_rate = min_tax_rate
        self.max_tax_rate = max_tax_rate
        self.tax_offsets = tax_offsets
        self.taxable_incomes = taxable_incomes

        self.tax_offset = 0
        self.taxable_income = 0

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
        self.tax_offset = 0
        self.taxable_income = 0
        for expense in self.tax_offsets:
            self.tax_offset += self.get_prop(expense, "expenses")
        for income in self.taxable_incomes:
            self.taxable_income += self.get_prop(income, "income")
        self.taxable_income -= self.tax_offset
        self.taxable_income = max(0, self.taxable_income)
        self.expenses = self.calcualte_tax(taxable_income=self.taxable_income, total_inflation=total_inflation)

        # TODO put into config
        # job, pension
        # insurances = self.get_prop("main.insurances.InsuranceHealth", "expenses")
        # insurances += self.get_prop("main.insurances.InsuranceNursingCare", "expenses")
        # insurances += self.get_prop("main.insurances.InsurancePension", "expenses")
        # insurances += self.get_prop("main.insurances.InsuranceUnemployment", "expenses")

        self.df_row["tax"] = self.expenses
        self.df_row["tax_offset"] = self.tax_offset
