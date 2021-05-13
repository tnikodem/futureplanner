import pytest

from fup.core.config import ModuleConfig

from fup.core.module import Module
from fup.modules.main.environment import Inflation
from fup.modules.main.insurances import InsuranceHealth, InsurancePension, InsuranceNursingCare, InsuranceUnemployment


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
    default_manager.add_module(ModuleConfig(name="pension", module_config=module_config, module_class=InsurancePension))
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
    default_manager.add_module(ModuleConfig(name="main.insurances.InsurancePension", module_config={"income": 0},
                                            module_class=Module))

    default_manager.add_module(ModuleConfig(name="health", module_config={"fraction_of_income": 0.073,
                                                                          }, module_class=InsuranceHealth))
    default_manager.next_year()
    assert default_manager.expenses == 10000 * 0.073


def test_insurance_nursing_care(default_manager):
    default_manager.add_module(ModuleConfig(name="main.work.Job", module_config={"income": 30000},
                                            module_class=Module))
    default_manager.add_module(ModuleConfig(name="main.insurances.InsurancePension", module_config={"income": 10000},
                                            module_class=Module))

    default_manager.add_module(ModuleConfig(name="care", module_config={"fraction_of_income": 0.0165,
                                                                        "retirement_factor": 2
                                                                        }, module_class=InsuranceNursingCare))
    default_manager.next_year()
    assert default_manager.expenses == pytest.approx(40000 * 0.0165)
    default_manager.profile.retired = True
    default_manager.next_year()
    assert default_manager.expenses == pytest.approx(40000 * 0.0165 * 2)


def test_insurance_unemployment(default_manager):
    default_manager.add_module(ModuleConfig(name="main.work.Job", module_config={"income": 30000,
                                                                                 "unemployed_months": 0,
                                                                                 "unemployed_since": 0},
                                            module_class=Module))

    default_manager.add_module(ModuleConfig(name="care", module_config={"fraction_of_income": 0.024 * 0.5,
                                                                        "months_you_get_unemployment_money": 12,
                                                                        "salary_fraction": 0.5
                                                                        }, module_class=InsuranceUnemployment))
    default_manager.next_year()
    assert default_manager.income == 0
    assert default_manager.expenses == pytest.approx(30000 * 0.024 * 0.5)

    default_manager.get_module("main.work.Job").unemployed_months = 6
    default_manager.next_year()
    assert default_manager.income == pytest.approx(30000 * 0.5)  # TODO check number with reality
    assert default_manager.expenses == pytest.approx(30000 * 0.024 * 0.5)

    default_manager.get_module("main.work.Job").unemployed_since = 15
    default_manager.next_year()
    assert default_manager.income == pytest.approx(15000 * 0.5)  # TODO check number with reality
    assert default_manager.expenses == pytest.approx(30000 * 0.024 * 0.5)
