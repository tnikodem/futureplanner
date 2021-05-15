import pytest
import random

from fup.core.config import ModuleConfig
from fup.modules.main.environment import Inflation


def test_inflation(default_manager):
    module_config = {"inflation_mean": 2, "inflation_std": 1}
    default_manager.add_module(ModuleConfig(name="inflation", module_config=module_config, module_class=Inflation))
    # next year
    default_manager.next_year()
    assert default_manager.df_row["inflation"] == 1.02
    assert default_manager.df_row["total_inflation"] == 1.02
    # random next year
    random.seed(42)
    default_manager.config["simulation"]["random"] = True
    default_manager.next_year()
    assert default_manager.df_row["inflation"] == pytest.approx(1.018559)
    assert default_manager.df_row["total_inflation"] == pytest.approx(1.02 * 1.018559)
