import pytest
import random

from fup.core.config import BluePrint
from fup.modules.main.environment import Inflation


def test_inflation(default_manager):
    build_config = {"inflation_mean": 2, "inflation_std": 1}
    default_manager.add_module(BluePrint(name="inflation", build_config=build_config, build_class=Inflation))
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
