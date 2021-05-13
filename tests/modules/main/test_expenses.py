from fup.core.config import ModuleConfig
from fup.modules.main.environment import Inflation
from fup.modules.main.expenses import InflationSensitive, InflationSensitiveVariable


def test_inflation_sensitive(default_manager):
    module_config = {"inflation_mean": 10, "inflation_std": 1}
    default_manager.add_module(ModuleConfig(name="main.environment.Inflation", module_config=module_config,
                                            module_class=Inflation))
    default_manager.add_module(ModuleConfig(name="test", module_config={"start_expenses": 1000,
                                                                        "info_name": "test"
                                                                        }, module_class=InflationSensitive))
    default_manager.add_module(ModuleConfig(name="test2", module_config={"start_expenses": 0,
                                                                         }, module_class=InflationSensitive))
    df_row = default_manager.get_df_row()
    assert df_row["test"] == 0
    # next year
    default_manager.next_year()
    df_row = default_manager.get_df_row()
    assert df_row["test"] == 1100
    assert default_manager.expenses == 1100


def test_inflation_sensitive_variable(default_manager):
    module_config = {"inflation_mean": 10, "inflation_std": 1}
    default_manager.add_module(ModuleConfig(name="main.environment.Inflation", module_config=module_config,
                                            module_class=Inflation))
    default_manager.add_module(ModuleConfig(name="test", module_config={"start_expenses": 1000,
                                                                        "info_name": "test"
                                                                        }, module_class=InflationSensitiveVariable))
    default_manager.add_module(ModuleConfig(name="test2", module_config={"start_expenses": 0,
                                                                         }, module_class=InflationSensitiveVariable))
    df_row = default_manager.get_df_row()
    assert df_row["test"] == 0
    # next year
    default_manager.next_year()
    df_row = default_manager.get_df_row()
    assert df_row["test"] == 2200
    assert default_manager.expenses == 2200
