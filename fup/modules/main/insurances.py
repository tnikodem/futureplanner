from fup.core.module import ChangeModule


class Health(ChangeModule):
    def next_year(self):
        inflation = self.get_prop("main.environment.Inflation", "inflation")
        self.income_threshold *= inflation
        income = self.get_prop("main.work.Job", "income") + self.get_prop("main.insurances.Pension", "income")
        capped_income = min(income, self.income_threshold)
        self.expenses = capped_income * self.fraction_of_income


class NursingCare(ChangeModule):
    def next_year(self):
        inflation = self.get_prop("main.environment.Inflation", "inflation")
        self.income_threshold *= inflation
        income = self.get_prop("main.work.Job", "income") + self.get_prop("main.insurances.Pension", "income")
        capped_income = min(income, self.income_threshold)
        if self.manager.profile.retired:
            self.expenses = capped_income * self.fraction_of_income * self.retirement_factor
        else:
            self.expenses = capped_income * self.fraction_of_income


class Pension(ChangeModule):
    @property
    def expected_income(self):
        # without inflation => inflation normalized income
        # expect to have similar income until retirement
        job_income = self.get_prop("main.work.Job", "income")
        capped_income = min(job_income, self.income_threshold)
        new_entgeldpunkte = capped_income / self.durchschnittseinkommen
        years_till_retirement = max((self.config["profile"]["retirement_year"] - self.manager.year), 0)
        expected_entgeldpunkte = self.entgeltpunkte + years_till_retirement * new_entgeldpunkte
        return expected_entgeldpunkte * self.rentenwert * 12

    def next_year(self):
        inflation = self.get_prop("main.environment.Inflation", "inflation")
        job_income = self.get_prop("main.work.Job", "income")
        self.rentenwert *= inflation
        self.durchschnittseinkommen *= inflation
        self.income_threshold *= inflation
        if not self.manager.profile.retired:
            capped_income = min(job_income, self.income_threshold)
            self.entgeltpunkte += capped_income / self.durchschnittseinkommen
            self.expenses = self.fraction_of_income * capped_income
        else:
            self.income = self.entgeltpunkte * self.rentenwert * 12


class Unemployment(ChangeModule):
    def next_year(self):
        birth_year = self.config["profile"]["birth_year"]
        salary_per_month = self.get_prop("main.work.Job", "salary_per_month")
        job_income = self.get_prop("main.work.Job", "income")
        unemployed_months = self.get_prop("main.work.Job", "unemployed_months")
        unemployed_months_this_year = self.get_prop("main.work.Job", "unemployed_months_this_year")
        inflation = self.get_prop("main.environment.Inflation", "inflation")

        self.income_threshold *= inflation

        capped_income = min(job_income, self.income_threshold)

        # Paying money
        if self.manager.profile.retired:
            self.expenses = capped_income * self.fraction_of_income * self.retirement_factor
        else:
            self.expenses = capped_income * self.fraction_of_income

        # Getting money
        if unemployed_months_this_year > 0:
            capped_salary_per_month = min(salary_per_month, self.income_threshold / 12)
            months_you_get_unemployment_money = self.months_you_get_unemployment_money
            if self.manager.year - birth_year > 54:
                months_you_get_unemployment_money = 24
            month_you_get_money = unemployed_months_this_year
            if unemployed_months > months_you_get_unemployment_money:
                month_you_get_money -= (unemployed_months - months_you_get_unemployment_money)
            month_you_get_money = max(month_you_get_money, 0)

            # TODO better formula to get unemployment money
            self.income = month_you_get_money * capped_salary_per_month * self.salary_fraction
