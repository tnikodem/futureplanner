import pytest
import random
import pandas as pd

from fup.core.config import BluePrint
from fup.core.module import AssetModule
from fup.modules.main.environment import Inflation
from fup.modules.main.work import Job
from fup.modules.events.crisis import OilCrisis1973


def test_oil_crisis_1973_fixed_year(default_manager):
    manager = default_manager
    crisis_config = {
        "start_year": 2002
    }
    manager.add_module(BluePrint(name="crisis", build_config=crisis_config, build_class=OilCrisis1973))
    build_config = {"inflation_mean": 2, "inflation_std": 0}
    default_manager.add_module(BluePrint(name="main.environment.Inflation", build_config=build_config,
                                         build_class=Inflation))
    job_build_config = {
        "start_income": 30000,
        "unemployed_months": 0,
        "prob_lose_job": 0.05,  # per month
        "prob_find_job": 0.1,  # per month
    }
    default_manager.add_module(BluePrint(name="main.work.Job", build_config=job_build_config, build_class=Job))
    manager.add_module(BluePrint(name="assets.resources.Gold", build_config={"start_money_value": 500},
                                 build_class=AssetModule))
    manager.add_module(BluePrint(name="assets.stocks.Stocks", build_config={"start_money_value": 500},
                                 build_class=AssetModule))

    # TODO refactor, this looks very similar to the run_simulation method
    rows = []
    for i in range(5):
        default_manager.next_year()
        rows += [default_manager.df_row]
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
    manager.add_module(BluePrint(name="crisis", build_config=crisis_config, build_class=OilCrisis1973))

    build_config = {"inflation_mean": 2, "inflation_std": 0}
    default_manager.add_module(BluePrint(name="main.environment.Inflation", build_config=build_config,
                                         build_class=Inflation))
    job_build_config = {
        "start_income": 30000,
        "unemployed_months": 0,
        "prob_lose_job": 0.05,  # per month
        "prob_find_job": 0.1,  # per month
    }
    default_manager.add_module(BluePrint(name="main.work.Job", build_config=job_build_config, build_class=Job))
    manager.add_module(BluePrint(name="assets.resources.Gold", build_config={"start_money_value": 500},
                                 build_class=AssetModule))
    manager.add_module(BluePrint(name="assets.stocks.Stocks", build_config={"start_money_value": 500},
                                 build_class=AssetModule))

    rows = []
    for i in range(8):
        default_manager.next_year()
        rows += [default_manager.df_row]
    df = pd.DataFrame(rows)

    assert df["event"].notnull().sum() == 4
    assert (df["inflation"] != 1.02).sum() == 3
    assert df["inflation"].max() == pytest.approx(1.111818)
    assert default_manager.get_module("assets.resources.Gold").money_value == pytest.approx(825)
    assert default_manager.get_module("assets.stocks.Stocks").money_value == pytest.approx(325.39682539)
