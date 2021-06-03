import pytest

from fup.core.config import BluePrint
from fup.core.module import AssetModule

from fup.modules.main.investing import Investing


def test_investing(default_manager):
    default_manager.add_module(BluePrint(name="test", build_config={"start_money_value": 1000},
                                         build_class=AssetModule))
    default_manager.add_module(BluePrint(name="test2", build_config={"start_money_value": 100},
                                         build_class=AssetModule))
    build_config = {
        "assets_ratios": {
            "test": 0.4,
            "test2": 0.1,
        },
    }
    default_manager.add_module(BluePrint(name="investing", build_config=build_config, build_class=Investing))
    default_manager.next_year()
    assert default_manager.total_assets == pytest.approx(1000 + 100)
    assert default_manager.get_module("test").money_value == pytest.approx(0.4 * 1100)
    assert default_manager.get_module("test2").money_value == pytest.approx(0.1 * 1100)
