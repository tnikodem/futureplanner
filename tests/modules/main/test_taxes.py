import pytest

from fup.core.config import ModuleConfig

from fup.core.module import Module
from fup.modules.main.environment import Inflation
from fup.modules.main.taxes import Taxes
from fup.modules.main.insurances import Health, Pension, NursingCare, Unemployment


# https://www.gevestor.de/details/steuersatz-in-deutschland-646731.html
# Tax in 2019, TODO update to 2020?!
def calc_tax(income):
    limit1 = 9168
    limit2 = 14254
    par2_a = 980.14
    par2_b = 1400
    limit3 = 54690
    par3_a = 216.16
    par3_b = 2397
    par3_c = 965.58
    limit4 = 265326
    par4_a = 0.42
    par4_b = 8780.90
    par5_a = 0.45
    par5_b = 16740.68
    if income < limit1:
        return 0
    if income < limit2:
        return (par2_a * ((income - limit1) / 10000) + par2_b) * ((income - limit1) / 10000)
    if income < limit3:
        return (par3_a * ((income - limit2) / 10000) + par3_b) * ((income - limit2) / 10000) + par3_c
    if income < limit4:
        return income * par4_a - par4_b
    return income * par5_a - par5_b


inflation_module_config = {"inflation_mean": 0, "inflation_std": 1}

pension_config = {
        "entgeltpunkte": 0,  # your points
        "rentenwert": 34.19,  # €/Entgeltpunkt/month, 2020
        "durchschnittseinkommen": 40551,  # € per year, 2020
        "fraction_of_income": 0.186 * 0.5,  # 2020  (half employer, half employee)
        "income_threshold": 82800,  # € per year, 2020
}

unemployed_config = {"fraction_of_income": 0.024 * 0.5,
                     "retirement_factor": 0,
                     "income_threshold": 82800,

                     "months_you_get_unemployment_money": 12,
                     "salary_fraction": 0.8 * 0.6,  # ~50%
                     }


# https://www.lohn-info.de/durchschnittssteuersatz_grenzsteuersatz.html
tax_module_config = {
    # linear interpolation between points
    "tax_rates": [
                    {"taxable_income": 0+9168, "tax_rate": 0.},
                    {"taxable_income": 3000+9168, "tax_rate": 0.04},
                    {"taxable_income": 8000+9168, "tax_rate": 0.1},
                    {"taxable_income": 15000+9168, "tax_rate": 0.147},
                    {"taxable_income": 26000+9168, "tax_rate": 0.20},
                    {"taxable_income": 42000+9168, "tax_rate": 0.25},
                    {"taxable_income": 64000+9168, "tax_rate": 0.303},
                    {"taxable_income": 116000+9168, "tax_rate": 0.355},
                    {"taxable_income": 325000+9168, "tax_rate": 0.405},
                    {"taxable_income": 827000+9168, "tax_rate": 0.43}],
    "taxable_incomes": ["main.work.Job", "main.insurances.Pension"],
    "tax_offsets": ["main.insurances.Health", "main.insurances.NursingCare",
                    "main.insurances.Pension", "main.insurances.Unemployment"]
}


def test_taxes(default_manager):
    for income in [0, 1e3, 1e4, 2e4, 3e4, 4e4, 5e4, 6e4, 1e5, 1e6]:
        # TODO this is a hack overwriting modules, is this good?!?!
        default_manager.add_module(ModuleConfig(name="main.environment.Inflation", module_config=inflation_module_config,
                                                module_class=Inflation))
        default_manager.add_module(ModuleConfig(name="main.work.Job",
                                                module_config={"income": income,
                                                               "salary_per_month": income/12,
                                                               "unemployed_months": 0,
                                                               "unemployed_months_this_year": 0,
                                                               }, module_class=Module))
        default_manager.add_module(ModuleConfig(name="main.insurances.Pension", module_config=pension_config,
                                                module_class=Pension))
        default_manager.add_module(ModuleConfig(name="main.insurances.Health",
                                                module_config={"fraction_of_income": 0.073,  # 2020
                                                               "income_threshold": 56250,  # €/year , 2020
                                                              }, module_class=Health))
        default_manager.add_module(ModuleConfig(name="main.insurances.NursingCare",
                                                module_config={"fraction_of_income": 0.0165,  # 2020
                                                               "retirement_factor": 2,
                                                               "income_threshold": 56250,  # €/year , 2020
                                                              }, module_class=NursingCare))
        default_manager.add_module(ModuleConfig(name="main.insurances.Unemployment", module_config=unemployed_config,
                                                module_class=Unemployment))
        default_manager.add_module(ModuleConfig(name="Tax", module_config=tax_module_config, module_class=Taxes))
        default_manager.next_year()

        if income < 56250:
            # TODO do not test Insurances thresholds here ?!
            expected_tax_offset = income * 0.186 * 0.5  # Pension
            expected_tax_offset += income * 0.073  # Health
            expected_tax_offset += income * 0.0165  # Nursing care
            expected_tax_offset += income * 0.024 * 0.5  # Unemployment
            assert default_manager.df_row["tax_offset"] == pytest.approx(expected_tax_offset)
        else:
            # TODO is this a problem that this is not checked for high incomes?!
            expected_tax_offset = income - default_manager.get_module("Tax").taxable_income

        assert default_manager.get_module("Tax").taxable_income == income - expected_tax_offset
        assert default_manager.df_row["tax"] == pytest.approx(calc_tax(income - expected_tax_offset), 1e-2)
        assert default_manager.df_row["expenses"] == pytest.approx(calc_tax(income - expected_tax_offset) + expected_tax_offset, 1e-2)

        # compare to https://www.brutto-netto-rechner.info/
        # print(f"""brutto: {income}  netto: {income - default_manager.df_row["expenses"] }  tax: {default_manager.df_row["tax"] }  social: {expected_tax_offset}""")
        # looks okay, but
        # TODO: church tax is missing!
