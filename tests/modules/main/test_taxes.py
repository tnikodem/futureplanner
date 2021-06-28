import pytest

from fup.core.config import BluePrint
from fup.core.module import Module
from fup.modules.main.environment import Inflation
from fup.modules.main.taxes import Taxes
from fup.modules.main.insurances import Health, Pension, NursingCare, Unemployment

# https://www.brutto-netto-rechner.info/
# 2019: tax class 1, no childs, without soli (as free limit is increased significantly)
bn_social_secutirty_contributions = {
    0: 0,
    1e3: 201.75,  # pension 93. unemployment 12.5, health 78.5, care 17.75
    1e4: 2017.5,  # pension 930, unemployment 125, health 785, care 177.5
    2e4: 4035,  # pension 1860, unemployment 250, health 1570, care 355
    3e4: 6052,  # pension 2790, unemployment 375, healh 2355, care 532.5
    4e4: 8070,  # pension 3720, unemployment 500, health 3140, care 710
    5e4: 10087,  # pension 4650, unemployment 625, health 3925, care 887
    6e4: 11570,  # pension 5580, unemployment 750, health 4274.33, care: 966
    1e5: 13723,  # pension 7477, unemployment 1005, health 4274, care 966
    1e6: 13723,  # pension 7477, unemployment 1005, health 4274, care 966
}
bn_tax = {
    0: 0,
    1e3: 0,
    1e4: 0,
    2e4: 1370,
    3e4: 3541,
    4e4: 6060,
    5e4: 8884,
    6e4: 12209,
    1e5: 28320,
    1e6: 428011
}
bn_tax_church = {
    3e4: 3540 + 283  # tax: 3540, church tax 283
}


# # https://www.gevestor.de/details/steuersatz-in-deutschland-646731.html
# # Tax in 2019
# # TODO why not use precise tax calcualtion??! Same performance and too complicated to generalize anyhow
# def calc_tax(income):
#     limit1 = 9168
#     limit2 = 14254
#     par2_a = 980.14
#     par2_b = 1400
#     limit3 = 54690
#     par3_a = 216.16
#     par3_b = 2397
#     par3_c = 965.58
#     limit4 = 265326
#     par4_a = 0.42
#     par4_b = 8780.90
#     par5_a = 0.45
#     par5_b = 16740.68
#     if income < limit1:
#         return 0
#     if income < limit2:
#         return (par2_a * ((income - limit1) / 10000) + par2_b) * ((income - limit1) / 10000)
#     if income < limit3:
#         return (par3_a * ((income - limit2) / 10000) + par3_b) * ((income - limit2) / 10000) + par3_c
#     if income < limit4:
#         return income * par4_a - par4_b
#     return income * par5_a - par5_b


inflation_build_config = {"inflation_mean": 1, "inflation_std": 0.01}

pension_config = {"entgeltpunkte": 0,  # your points
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
tax_build_config = {
    # linear interpolation between points
    "tax_rates": [{"taxable_income": 0 + 9168, "tax_rate": 0.},
                  {"taxable_income": 3000 + 9168, "tax_rate": 0.04},
                  {"taxable_income": 8000 + 9168, "tax_rate": 0.1},
                  {"taxable_income": 15000 + 9168, "tax_rate": 0.147},
                  {"taxable_income": 26000 + 9168, "tax_rate": 0.20},
                  {"taxable_income": 42000 + 9168, "tax_rate": 0.25},
                  {"taxable_income": 64000 + 9168, "tax_rate": 0.303},
                  {"taxable_income": 116000 + 9168, "tax_rate": 0.355},
                  {"taxable_income": 325000 + 9168, "tax_rate": 0.405},
                  {"taxable_income": 827000 + 9168, "tax_rate": 0.43}],
    "taxable_incomes": ["main.work.Job", "main.insurances.Pension"],
    "tax_offsets": ["main.insurances.Health", "main.insurances.NursingCare",
                    "main.insurances.Pension", "main.insurances.Unemployment"]
}


def test_taxes(default_manager):
    for income in [0, 1e3, 1e4, 2e4, 3e4, 4e4, 5e4, 6e4, 1e5, 1e6]:
        # TODO this is a hack overwriting modules, is this good?!?!
        default_manager.add_module(BluePrint(name="main.environment.Inflation", build_config=inflation_build_config,
                                             build_class=Inflation))
        default_manager.add_module(BluePrint(name="main.work.Job",
                                             build_config={"income": income,
                                                           "salary_per_month": income / 12,
                                                           "unemployed_months": 0,
                                                           "unemployed_months_this_year": 0,
                                                           }, build_class=Module))
        default_manager.add_module(BluePrint(name="main.insurances.Pension", build_config=pension_config,
                                             build_class=Pension))
        default_manager.add_module(BluePrint(name="main.insurances.Health", build_class=Health,
                                             build_config={"fraction_of_income": 0.073,  # 2020
                                                           "income_threshold": 56250,  # €/year , 2020
                                                           },))
        default_manager.add_module(BluePrint(name="main.insurances.NursingCare", build_class=NursingCare,
                                             build_config={"fraction_of_income": 0.0165,  # 2020
                                                           "retirement_factor": 2,
                                                           "income_threshold": 56250,  # €/year , 2020
                                                           },))
        default_manager.add_module(BluePrint(name="main.insurances.Unemployment", build_config=unemployed_config,
                                             build_class=Unemployment))
        default_manager.add_module(BluePrint(name="Tax", build_config=tax_build_config, build_class=Taxes))
        default_manager.next_year()

        assert default_manager.get_module("Tax").taxable_income == \
               pytest.approx(income - bn_social_secutirty_contributions[income], 1e-1)
        assert default_manager.df_row["tax"] == pytest.approx(bn_tax[income], 1e-1)
        expenses = bn_tax[income] + bn_social_secutirty_contributions[income]
        assert default_manager.df_row["expenses"] == pytest.approx(expenses, 1e-1)


def test_church_tax(default_manager):
    income = 26000 + 9168
    tax_build_config = {
        # linear interpolation between points
        "tax_rates": [{"taxable_income": 0 + 9168, "tax_rate": 0.},
                      {"taxable_income": 3000 + 9168, "tax_rate": 0.04},
                      {"taxable_income": 8000 + 9168, "tax_rate": 0.1},
                      {"taxable_income": 15000 + 9168, "tax_rate": 0.147},
                      {"taxable_income": 26000 + 9168, "tax_rate": 0.20},
                      {"taxable_income": 42000 + 9168, "tax_rate": 0.25},
                      {"taxable_income": 64000 + 9168, "tax_rate": 0.303},
                      {"taxable_income": 116000 + 9168, "tax_rate": 0.355},
                      {"taxable_income": 325000 + 9168, "tax_rate": 0.405},
                      {"taxable_income": 827000 + 9168, "tax_rate": 0.43}],
        "taxable_incomes": ["main.work.Job"],
        "tax_offsets": [],
        "church_tax_rate": 8
    }

    default_manager.add_module(BluePrint(name="main.environment.Inflation", build_config=inflation_build_config,
                                         build_class=Inflation))
    default_manager.add_module(BluePrint(name="main.work.Job",
                                         build_config={"income": income,
                                                       "salary_per_month": income / 12,
                                                       "unemployed_months": 0,
                                                       "unemployed_months_this_year": 0,
                                                       }, build_class=Module))
    default_manager.add_module(BluePrint(name="Tax", build_config=tax_build_config, build_class=Taxes))
    default_manager.next_year()

    assert default_manager.df_row["tax"] == pytest.approx(income*0.2*1.08)
