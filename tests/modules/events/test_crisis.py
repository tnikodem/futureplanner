import pytest
import random
import pandas as pd

from fup.core.config import ModuleConfig
from fup.core.module import AssetModule
from fup.modules.main.environment import Inflation
from fup.modules.main.work import Job
from fup.modules.events.crisis import OilCrisis1973


def test_oil_crisis_1973_fixed_year(default_manager):
    manager = default_manager

    crisis_config = {
        "start_year": 2002
    }
    manager.add_module(ModuleConfig(name="crisis", module_config=crisis_config, module_class=OilCrisis1973))

    module_config = {"inflation_mean": 2, "inflation_std": 0}
    default_manager.add_module(ModuleConfig(name="main.environment.Inflation", module_config=module_config,
                                            module_class=Inflation))
    job_module_config = {
        "start_income": 30000,
        "unemployed_months": 0,
        "prob_lose_job": 0.05,  # per month
        "prob_find_job": 0.1,  # per month
    }
    default_manager.add_module(ModuleConfig(name="main.work.Job", module_config=job_module_config, module_class=Job))
    manager.add_module(ModuleConfig(name="assets.resources.Gold", module_config={"start_money_value": 500},
                                    module_class=AssetModule))
    manager.add_module(ModuleConfig(name="assets.stocks.Stocks", module_config={"start_money_value": 500},
                                    module_class=AssetModule))

    rows = []
    for i in range(5):
        default_manager.next_year()
        rows += [default_manager.get_df_row()]
    df = pd.DataFrame(rows)

    assert df["event"].notnull().sum() == 4
    assert (df["inflation"] != 1.02).sum() == 3
    assert df["inflation"].max() == pytest.approx(1.111818)
    assert default_manager.get_module("assets.resources.Gold").money_value == pytest.approx(825)
    assert default_manager.get_module("assets.stocks.Stocks").money_value == pytest.approx(325.39682539)


def test_oil_crisis_1973_random(default_manager):
    manager = default_manager
    default_manager.config["simulation"]["random"] = True
    random.seed(42)

    crisis_config = {
        "probability": 0.3
    }
    manager.add_module(ModuleConfig(name="crisis", module_config=crisis_config, module_class=OilCrisis1973))

    module_config = {"inflation_mean": 2, "inflation_std": 0}
    default_manager.add_module(ModuleConfig(name="main.environment.Inflation", module_config=module_config,
                                            module_class=Inflation))
    job_module_config = {
        "start_income": 30000,
        "unemployed_months": 0,
        "prob_lose_job": 0.05,  # per month
        "prob_find_job": 0.1,  # per month
    }
    default_manager.add_module(ModuleConfig(name="main.work.Job", module_config=job_module_config, module_class=Job))
    manager.add_module(ModuleConfig(name="assets.resources.Gold", module_config={"start_money_value": 500},
                                    module_class=AssetModule))
    manager.add_module(ModuleConfig(name="assets.stocks.Stocks", module_config={"start_money_value": 500},
                                    module_class=AssetModule))

    rows = []
    for i in range(8):
        default_manager.next_year()
        rows += [default_manager.get_df_row()]
    df = pd.DataFrame(rows)

    assert df["event"].notnull().sum() == 4
    assert (df["inflation"] != 1.02).sum() == 3
    assert df["inflation"].max() == pytest.approx(1.111818)
    assert default_manager.get_module("assets.resources.Gold").money_value == pytest.approx(825)
    assert default_manager.get_module("assets.stocks.Stocks").money_value == pytest.approx(325.39682539)
