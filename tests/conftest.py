import pytest
from fup.core.config import ModuleConfig
from fup.core.manager import Manager
from fup.profiles import profiles
from fup.core.module import AssetModule


@pytest.fixture(scope="function")
def default_config():
    return {
        "simulation": {
            "start_year": 2000,
            "end_year": 2100,
            "start_income": 42000,
            "start_expenses": 35000,
            "random": False,
        },
        "profile": {
            "birth_year": 2000,
            "retirement_year": 2050,
            "retirement_factor": 1,
        }
    }


@pytest.fixture(scope="function")
def default_manager(default_config):
    module_list = [
        ModuleConfig(name="assets.money.Money", module_config={"start_money_value": 0}, module_class=AssetModule),
    ]

    return Manager(config=default_config, module_list=module_list, profile_class=profiles.Test)
