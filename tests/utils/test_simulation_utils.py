import pytest
from fup.profiles import profiles
from fup.utils.simulation_utils import get_sorted_module_blueprints, get_start_values, run_simulations


def test_get_sorted_module_blueprints(modules_config):
    sorted_module_config_list = get_sorted_module_blueprints(modules_config)
    assert len(sorted_module_config_list) == 6
    assert sorted_module_config_list[0].name == "stocks"
    assert sorted_module_config_list[1].name == "assets.money.Money"
    assert sorted_module_config_list[2].name == "main.environment.Inflation"
    assert sorted_module_config_list[3].name == "Job"
    assert sorted_module_config_list[4].name == "main.taxes.Taxes"
    assert sorted_module_config_list[5].name == "main.investing.Investing"


def test_get_start_values(modules_config):
    df = get_start_values(config=modules_config)
    # Don't do tax calculation check here
    job_income = df.query("name == 'Job'")["income"].values[0]
    tax = df.query("name == 'main.taxes.Taxes'")["expenses"].values[0]
    money = 1000 + job_income - tax
    assert df["value"].sum() == pytest.approx(money)
    assert df.query("name == 'assets.money.Money'")["value"].values[0] == pytest.approx(0.6 * money)
    assert df.query("name == 'stocks'")["value"].values[0] == pytest.approx(0.4 *money)


def test_run_simulations(modules_config):
    df, df_stats = run_simulations(config=modules_config, profile_class=profiles.FullInvestment, runs=2)
    assert "year" in df.columns
    assert "run" in df.columns
    assert list(df["run"].unique()) == [0, 1]
    assert len(df) == pytest.approx(2 * 20)
