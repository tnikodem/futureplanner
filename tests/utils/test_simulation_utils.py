import pytest
from fup.profiles import profiles
from fup.utils.simulation_utils import get_sorted_module_config_list, get_start_values


def test_get_sorted_modules(modules_config):
    sorted_module_config_list = get_sorted_module_config_list(modules_config)
    assert len(sorted_module_config_list) == 5
    assert sorted_module_config_list[0].name == "stocks"
    assert sorted_module_config_list[1].name == "assets.money.Money"
    assert sorted_module_config_list[2].name == "main.environment.Inflation"
    assert sorted_module_config_list[3].name == "Job"
    assert sorted_module_config_list[4].name == "main.investing.Investing"


def test_get_start_values(modules_config):
    # 1000€ start money + 42840(1.02*42000€) income
    df = get_start_values(config=modules_config, profile_class=profiles.Test)
    assert df.query("name == 'Job'")["income"].values[0] == pytest.approx(1.02*42000)
    assert df["value"].sum() == pytest.approx(1000 + 1.02*42000)
    assert df.query("name == 'assets.money.Money'")["value"].values[0] == pytest.approx(0.6 * (1000 + 1.02*42000))
    assert df.query("name == 'stocks'")["value"].values[0] == pytest.approx(0.4 * (1000 + 1.02*42000))
