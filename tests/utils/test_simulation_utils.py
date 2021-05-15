import pytest
from fup.profiles import profiles
from fup.utils.simulation_utils import get_sorted_module_config_list, get_start_values, run_simulations


def test_get_sorted_modules(modules_config):
    sorted_module_config_list = get_sorted_module_config_list(modules_config)
    assert len(sorted_module_config_list) == 6
    assert sorted_module_config_list[0].name == "stocks"
    assert sorted_module_config_list[1].name == "assets.money.Money"
    assert sorted_module_config_list[2].name == "main.environment.Inflation"
    assert sorted_module_config_list[3].name == "Job"
    assert sorted_module_config_list[4].name == "main.taxes.Taxes"
    assert sorted_module_config_list[5].name == "main.investing.Investing"


def test_get_start_values(modules_config):
    # 1000€ start money + 42840(1.02*42000€) income - 30% tax
    df = get_start_values(config=modules_config, profile_class=profiles.Test)
    assert df.query("name == 'Job'")["income"].values[0] == pytest.approx(1.02 * 42000)

    assert df["value"].sum() == pytest.approx(1000 + 1.02 * 42000 * 0.7)
    assert df.query("name == 'assets.money.Money'")["value"].values[0] == pytest.approx(
        0.6 * (1000 + 1.02 * 42000 * 0.7))
    assert df.query("name == 'stocks'")["value"].values[0] == pytest.approx(0.4 * (1000 + 1.02 * 42000 * 0.7))


def test_run_simulations(modules_config):
    df, df_stats = run_simulations(config=modules_config, profile_class=profiles.Test, runs=2)
    assert "year" in df.columns
    assert "run" in df.columns
    assert list(df["run"].unique()) == [0, 1]
    assert len(df) == pytest.approx(2 * 20)
