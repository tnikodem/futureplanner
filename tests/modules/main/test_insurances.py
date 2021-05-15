import random
import pytest

from fup.core.config import ModuleConfig

from fup.core.module import Module
from fup.modules.main.environment import Inflation
from fup.modules.main.work import Job
from fup.modules.main.insurances import Health, Pension, NursingCare, Unemployment


def test_insurance_pension(default_manager):
    module_config = {"inflation_mean": 0, "inflation_std": 1}
    default_manager.add_module(ModuleConfig(name="main.environment.Inflation", module_config=module_config,
                                            module_class=Inflation))
    default_manager.add_module(ModuleConfig(name="main.work.Job", module_config={"income": 38901/2},
                                            module_class=Module))
    module_config = {
        "entgeltpunkte": 10,
        "rentenwert":  33 * 12,  # 2019
        "durchschnittseinkommen": 38901,  # 2019
        "fraction_of_income": 0.186 * 0.5,
    }
    # paying money
    default_manager.add_module(ModuleConfig(name="pension", module_config=module_config, module_class=Pension))
    assert default_manager.get_module("pension").expected_income == pytest.approx(13860.0)  # TODO test with real numbers
    default_manager.next_year()
    assert default_manager.get_module("pension").entgeltpunkte == pytest.approx(10.5)
    assert default_manager.expenses == pytest.approx(1808.8965)
    # getting money
    default_manager.profile.retired = True
    default_manager.next_year()
    assert default_manager.expenses == 0
    assert default_manager.income == 4158


def test_insurance_health(default_manager):
    default_manager.add_module(ModuleConfig(name="main.work.Job", module_config={"income": 10000},
                                            module_class=Module))
    default_manager.add_module(ModuleConfig(name="main.insurances.Pension", module_config={"income": 0},
                                            module_class=Module))

    default_manager.add_module(ModuleConfig(name="health", module_config={"fraction_of_income": 0.073,
                                                                          }, module_class=Health))
    default_manager.next_year()
    assert default_manager.expenses == 10000 * 0.073


def test_insurance_nursing_care(default_manager):
    default_manager.add_module(ModuleConfig(name="main.work.Job", module_config={"income": 30000},
                                            module_class=Module))
    default_manager.add_module(ModuleConfig(name="main.insurances.Pension", module_config={"income": 10000},
                                            module_class=Module))

    default_manager.add_module(ModuleConfig(name="care", module_config={"fraction_of_income": 0.0165,
                                                                        "retirement_factor": 2
                                                                        }, module_class=NursingCare))
    default_manager.next_year()
    assert default_manager.expenses == pytest.approx(40000 * 0.0165)
    default_manager.profile.retired = True
    default_manager.next_year()
    assert default_manager.expenses == pytest.approx(40000 * 0.0165 * 2)


def test_unemployment(default_manager):
    inflation_module_config = {"inflation_mean": 2, "inflation_std": 0}
    default_manager.add_module(ModuleConfig(name="main.environment.Inflation", module_config=inflation_module_config,
                                            module_class=Inflation))
    job_module_config = {
        "start_income": 30000,
        "unemployed_months": 0,
        "prob_lose_job": .1,
        "prob_find_job": 0.,
    }
    default_manager.add_module(ModuleConfig(name="main.work.Job", module_config=job_module_config, module_class=Job))
    default_manager.add_module(ModuleConfig(name="unemployment",
                                            module_config={"fraction_of_income": 0.024 * 0.5,
                                                           "months_you_get_unemployment_money": 12,
                                                           "salary_fraction": 0.5
                                                           },
                                            module_class=Unemployment))
    default_manager.next_year()
    assert default_manager.income == 30000 * 1.02
    assert default_manager.expenses == pytest.approx(30000 * 1.02 * 0.024 * 0.5)

    random.seed(42)
    default_manager.config["simulation"]["random"] = True
    default_manager.next_year()
    assert default_manager.get_module("main.work.Job").unemployed_months == 7
    assert default_manager.get_module("main.work.Job").unemployed_months_this_year == 7
    assert default_manager.get_module("unemployment").income == pytest.approx(1.02**2 * 30000 * 0.5 * 7/12)
    # second year 12 month limit reached
    default_manager.next_year()
    assert default_manager.get_module("main.work.Job").unemployed_months == 19
    assert default_manager.get_module("main.work.Job").unemployed_months_this_year == 12
    assert default_manager.get_module("unemployment").income == pytest.approx(1.02**3 * 30000 * 0.5 * 5/12)
    # TODO check with reality, how long do you geht unemployment money??!
