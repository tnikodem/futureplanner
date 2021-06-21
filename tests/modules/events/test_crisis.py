import pytest
import random
import pandas as pd

from fup.core.config import BluePrint
from fup.core.module import AssetModule
from fup.modules.main.environment import Inflation
from fup.modules.main.work import Job
from fup.modules.events.crisis import OilCrisis1973, LostDecadeJapan1991, GreatRecession2007


def test_great_recession_2007(default_manager):
    manager = default_manager
    crisis_config = {
        "start_year": 2002
    }
    manager.add_module(BluePrint(name="crisis", build_config=crisis_config, build_class=GreatRecession2007))
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
    for i in range(20):
        default_manager.next_year()
        df_row = default_manager.df_row
        df_row["stocks_asset_value"] = manager.get_module("assets.stocks.Stocks").asset_value
        df_row["gold_asset_value"] = manager.get_module("assets.resources.Gold").asset_value
        rows += [df_row]
    df = pd.DataFrame(rows)

    assert df["event"].notnull().sum() == 6
    assert df["inflation"].values[-1] == 1.02
    assert df["inflation"].min() == 0.995

    assert df["stocks_asset_value"].max() == pytest.approx(1.6, 1e-3)  # bubble max
    assert df["stocks_asset_value"].min() == pytest.approx(0.8, 1e-3)  # crash min
    assert df["stocks_asset_value"].values[-1] == pytest.approx(1.2, 1e-3)

    assert df["gold_asset_value"].values[-1] == pytest.approx(1500 / 600, 1e-2)


def test_lost_decade_japan_1991(default_manager):
    manager = default_manager
    crisis_config = {
        "start_year": 2002
    }
    manager.add_module(BluePrint(name="crisis", build_config=crisis_config, build_class=LostDecadeJapan1991))
    build_config = {"inflation_mean": 2, "inflation_std": 0}
    default_manager.add_module(BluePrint(name="main.environment.Inflation", build_config=build_config,
                                         build_class=Inflation))
    manager.add_module(BluePrint(name="assets.resources.Gold", build_config={"start_money_value": 500},
                                 build_class=AssetModule))
    manager.add_module(BluePrint(name="assets.stocks.Stocks", build_config={"start_money_value": 500},
                                 build_class=AssetModule))

    # TODO refactor, this looks very similar to the run_simulation method
    rows = []
    for i in range(20):
        default_manager.next_year()
        df_row = default_manager.df_row
        df_row["stocks_asset_value"] = manager.get_module("assets.stocks.Stocks").asset_value
        df_row["gold_asset_value"] = manager.get_module("assets.resources.Gold").asset_value
        rows += [df_row]
    df = pd.DataFrame(rows)

    assert df["event"].notnull().sum() == 18

    assert df["inflation"].values[-1] == 1.02
    assert df["inflation"].max() == 1.03

    assert df["stocks_asset_value"].max() == pytest.approx(1.75, 1e-3)  # bubble max
    assert df["stocks_asset_value"].values[-1] == pytest.approx(0.65, 0.05)

    assert df["gold_asset_value"].max() == 1  # no bubble, only going down
    assert df["gold_asset_value"].values[-1] == pytest.approx(0.6, 1e-3)


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
