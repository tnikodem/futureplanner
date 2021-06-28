from fup.core.config import BluePrint
from fup.modules.main.environment import Inflation
from fup.modules.main.expenses import InflationSensitive, InflationSensitiveVariable


def test_inflation_sensitive_expenses(default_manager):
    build_config = {"inflation_mean": 1.1, "inflation_std": 0.01}
    default_manager.add_module(BluePrint(name="main.environment.Inflation", build_config=build_config,
                                         build_class=Inflation))
    default_manager.add_module(BluePrint(name="test", build_config={"start_expenses": 1000, "info_name": "test"},
                                         build_class=InflationSensitive))
    default_manager.add_module(BluePrint(name="test2", build_config={"start_expenses": 0},
                                         build_class=InflationSensitive))
    default_manager.next_year()
    assert default_manager.df_row["test"] == 1100
    assert default_manager.df_row["expenses"] == 1100


def test_inflation_sensitive_variable_expenses(default_manager):
    build_config = {"inflation_mean": 1.1, "inflation_std": 0.01}
    default_manager.profile.money_level = 10
    default_manager.add_module(BluePrint(name="main.environment.Inflation", build_config=build_config,
                                         build_class=Inflation))
    default_manager.add_module(BluePrint(name="test", build_config={"start_expenses": 1000, "info_name": "test"},
                                         build_class=InflationSensitiveVariable))
    default_manager.add_module(BluePrint(name="test2", build_config={"start_expenses": 0},
                                         build_class=InflationSensitiveVariable))
    default_manager.next_year()
    assert default_manager.df_row["test"] == 2200
    assert default_manager.df_row["expenses"] == 2200
