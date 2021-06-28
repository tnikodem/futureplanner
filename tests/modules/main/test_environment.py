import pytest
import random

from fup.core.config import BluePrint
from fup.modules.main.environment import Inflation


def test_inflation(default_manager):
    build_config = {"inflation_mean": 1.02, "inflation_std": 0.01}
    default_manager.add_module(BluePrint(name="inflation", build_config=build_config, build_class=Inflation))
    # next year
    default_manager.next_year()
    assert default_manager.df_row["inflation"] == 1.02
    assert default_manager.df_row["total_inflation"] == 1.02
    # random next year
    random.seed(42)
    default_manager.config["simulation"]["random"] = True
    default_manager.next_year()
    assert default_manager.df_row["inflation"] == pytest.approx(1.0185, 1e-3)
    assert default_manager.df_row["total_inflation"] == pytest.approx(1.02 * 1.0185, 1e-3)
