import random
import pytest

from fup.core.config import ModuleConfig
from fup.core.module import Module
from fup.modules.main.environment import Inflation
from fup.modules.main.work import Job
from fup.modules.main.insurances import Health, Pension, NursingCare, Unemployment


def test_pension(default_manager):
    """
      https://www.test.de/rentenversicherung-5156247-0/
      https://www.handelsblatt.com/politik/deutschland/rentenpunkte-erklaert-so-errechnen-sie-2021-mit-rentenpunkten-die-hoehe-ihrer-gesetzlichen-rente/26969926.html?ticket=ST-4923658-1gjQbaUz5TlgEFV2rId6-ap6
      https://www.finanztip.de/beitragsbemessungsgrenze/
    """
    module_config = {"inflation_mean": 0, "inflation_std": 1}
    default_manager.add_module(ModuleConfig(name="main.environment.Inflation", module_config=module_config,
                                            module_class=Inflation))
    default_manager.add_module(ModuleConfig(name="main.work.Job", module_config={"income": 0},
                                            module_class=Module))
    module_config = {
        "entgeltpunkte": 0,  # your points
        "rentenwert": 34.19,  # €/Entgeltpunkt/month, 2020
        "durchschnittseinkommen": 40551,  # € per year, 2020
        "fraction_of_income": 0.186 * 0.5,  # 2020  (half employer, half employee)
        "income_threshold": 82800,  # € per year, 2020
    }
    default_manager.add_module(ModuleConfig(name="pension", module_config=module_config, module_class=Pension))
    # Paying money
    # None
    default_manager.next_year()
    assert default_manager.get_module("pension").entgeltpunkte == pytest.approx(0)
    assert default_manager.df_row["expenses"] == pytest.approx(0)
    # Mean
    default_manager.get_module("main.work.Job").income = 40551
    default_manager.next_year()
    assert default_manager.get_module("pension").entgeltpunkte == pytest.approx(1)
    assert default_manager.df_row["expenses"] == pytest.approx(40551 * 0.186 * 0.5)
    # Above max
    default_manager.get_module("pension").entgeltpunkte = 0
    default_manager.get_module("main.work.Job").income = 100000
    default_manager.next_year()
    assert default_manager.get_module("pension").entgeltpunkte == pytest.approx(82800 / 40551)
    assert default_manager.df_row["expenses"] == pytest.approx(82800 * 0.186 * 0.5)

    # Getting money
    default_manager.profile.retired = True
    default_manager.get_module("pension").entgeltpunkte = 50
    default_manager.next_year()
    assert default_manager.df_row["expenses"] == 0
    assert default_manager.df_row["income"] == pytest.approx(34.19 * 12 * 50)


def test_pension_expected_income(default_manager):
    module_config = {"inflation_mean": 0, "inflation_std": 1}
    default_manager.add_module(ModuleConfig(name="main.environment.Inflation", module_config=module_config,
                                            module_class=Inflation))
    default_manager.add_module(ModuleConfig(name="main.work.Job", module_config={"income": 40551},
                                            module_class=Module))
    module_config = {
        "entgeltpunkte": 0,  # your points
        "rentenwert": 34.19,  # €/Entgeltpunkt/month, 2020
        "durchschnittseinkommen": 40551,  # € per year, 2020
        "fraction_of_income": 0.186 * 0.5,  # 2020  (half employer, half employee)
        "income_threshold": 82800,  # € per year, 2020
    }
    default_manager.add_module(ModuleConfig(name="pension", module_config=module_config, module_class=Pension))
    assert default_manager.get_module("pension").expected_income == pytest.approx(10 * 34.19 * 12)


def test_insurance_health(default_manager):
    """"
      https://www.krankenkassen.de/gesetzliche-krankenkassen/krankenkasse-beitrag/beitragsrechner/
      https://www.finanztip.de/beitragsbemessungsgrenze/
      ~14.6% (half employer, half employee)
    """

    inflation_module_config = {"inflation_mean": 0, "inflation_std": 0}
    default_manager.add_module(ModuleConfig(name="main.environment.Inflation", module_config=inflation_module_config,
                                            module_class=Inflation))
    default_manager.add_module(ModuleConfig(name="main.work.Job", module_config={"income": 10000},
                                            module_class=Module))
    default_manager.add_module(ModuleConfig(name="main.insurances.Pension", module_config={"income": 0},
                                            module_class=Module))

    default_manager.add_module(ModuleConfig(name="health", module_config={"fraction_of_income": 0.073,  # 2020
                                                                          "income_threshold": 56250,  # €/year , 2020
                                                                          }, module_class=Health))
    default_manager.next_year()
    assert default_manager.df_row["expenses"] == pytest.approx(10000 * 0.073)
    # Above max
    default_manager.get_module("main.work.Job").income = 200000
    default_manager.next_year()
    assert default_manager.df_row["expenses"] == pytest.approx(56250 * 0.073)


def test_insurance_nursing_care(default_manager):
    """"
      https://www.krankenkassen.de/gesetzliche-krankenkassen/krankenkasse-beitrag/beitragsrechner/
      https://www.finanztip.de/beitragsbemessungsgrenze/
      ~3.3% (half employer, half employee), full when retired
    """
    inflation_module_config = {"inflation_mean": 0, "inflation_std": 0}
    default_manager.add_module(ModuleConfig(name="main.environment.Inflation", module_config=inflation_module_config,
                                            module_class=Inflation))
    default_manager.add_module(ModuleConfig(name="main.work.Job", module_config={"income": 10000}, module_class=Module))
    default_manager.add_module(ModuleConfig(name="main.insurances.Pension", module_config={"income": 0},
                                            module_class=Module))

    default_manager.add_module(ModuleConfig(name="care", module_config={"fraction_of_income": 0.0165,  # 2020
                                                                        "retirement_factor": 2,
                                                                        "income_threshold": 56250,  # €/year , 2020
                                                                        }, module_class=NursingCare))
    # Standard
    default_manager.next_year()
    assert default_manager.df_row["expenses"] == pytest.approx(10000 * 0.0165)
    # Above max
    default_manager.get_module("main.work.Job").income = 200000
    default_manager.next_year()
    assert default_manager.df_row["expenses"] == pytest.approx(56250 * 0.0165)
    # Retired
    default_manager.profile.retired = True
    default_manager.get_module("main.work.Job").income = 0
    default_manager.get_module("main.insurances.Pension").income = 10000
    default_manager.next_year()
    assert default_manager.df_row["expenses"] == pytest.approx(10000 * 0.0165 * 2)


def test_unemployment(default_manager):
    """
        https://www.lohn-info.de/beitragsbemessungsgrenzen.html  -> same threshold as pension
        https://www.krankenkassenzentrale.de/wiki/arbeitslosenversicherung#
        ~ 2.4% (half employer, half employee), none when retired

        https://www.betanet.de/arbeitslosengeld.html
        https://www.arbeitsagentur.de/finanzielle-hilfen/arbeitslosengeld-anspruch-hoehe-dauer

        (smaller effects that are ignored at the moment)
        TODO: if unemployed there is also compensation
        TODO: in last 30 month you worked at least 12, minimum, maximum if full employed in last 24 months
        TODO: mean income of last 12 month, not normal salary per month

        income: (Gross income (max income_theshold) - 20%) * 60% ( 67% if you have a child)
        for 12 month,  12-24month if > 50-58years


    """
    inflation_module_config = {"inflation_mean": 0, "inflation_std": 0}
    default_manager.add_module(ModuleConfig(name="main.environment.Inflation", module_config=inflation_module_config,
                                            module_class=Inflation))
    job_module_config = {
        "start_income": 10000,
        "unemployed_months": 0,
        "prob_lose_job": 0.,
        "prob_find_job": 0.,
    }
    default_manager.add_module(ModuleConfig(name="main.work.Job", module_config=job_module_config, module_class=Job))

    unemployed_config = {"fraction_of_income": 0.024 * 0.5,
                         "retirement_factor": 0,
                         "income_threshold": 82800,

                         "months_you_get_unemployment_money": 12,
                         "salary_fraction": 0.8*0.6,  #  ~50%
                         }

    default_manager.add_module(ModuleConfig(name="unemployment", module_config=unemployed_config,
                                            module_class=Unemployment))

    # Paying money
    # Standard
    default_manager.next_year()
    assert default_manager.df_row["expenses"] == pytest.approx(10000 * 0.024 * 0.5)
    # Above max
    default_manager.get_module("main.work.Job").salary_per_month = 200000
    default_manager.next_year()
    assert default_manager.df_row["expenses"] == pytest.approx(82800 * 0.024 * 0.5)
    # Retired
    default_manager.profile.retired = True
    default_manager.next_year()
    assert default_manager.df_row["expenses"] == pytest.approx(0)

    # Getting Money
    # Standard
    default_manager.profile.retired = False
    default_manager.get_module("main.work.Job").salary_per_month = 2000
    default_manager.get_module("main.work.Job").unemployed_months_this_year = 12
    default_manager.get_module("main.work.Job").unemployed_months = 12
    default_manager.next_year()
    assert default_manager.df_row["income"] == pytest.approx(2000 * 12 * 0.8 * 0.6)
    # Above max
    default_manager.get_module("main.work.Job").salary_per_month = 200000
    default_manager.next_year()
    assert default_manager.df_row["income"] == pytest.approx(82800 * 0.8 * 0.6)
    # Retired
    default_manager.profile.retired = True
    default_manager.next_year()
    assert default_manager.df_row["income"] == pytest.approx(0)

    # Longer than 12 month
    default_manager.get_module("main.work.Job").salary_per_month = 200000
    default_manager.profile.retired = False
    default_manager.get_module("main.work.Job").unemployed_months_this_year = 12
    default_manager.get_module("main.work.Job").unemployed_months = 18
    default_manager.next_year()
    assert default_manager.df_row["income"] == pytest.approx(82800 * 0.5 * 0.8 * 0.6)

    # random
    random.seed(42)
    default_manager.config["simulation"]["random"] = True
    default_manager.get_module("main.work.Job").salary_per_month = 200000
    default_manager.get_module("main.work.Job").unemployed_months_this_year = 0
    default_manager.get_module("main.work.Job").unemployed_months = 0
    default_manager.get_module("main.work.Job").prob_lose_job = 0.2
    default_manager.next_year()
    unemployed_months = default_manager.get_module("main.work.Job").unemployed_months_this_year
    assert default_manager.get_module("unemployment").income == pytest.approx(82800 * 0.8 * 0.6 * unemployed_months/12)
