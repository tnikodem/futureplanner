import pytest

from fup.core.config import ModuleConfig

from fup.modules.assets.money import Money
from fup.modules.main.investing import Investing


def test_investing(default_manager):
    default_manager.add_module(ModuleConfig(name="test", module_config={"start_money_value": 1000,
                                                                        }, module_class=Money))
    default_manager.add_module(ModuleConfig(name="test2", module_config={"start_money_value": 100,
                                                                         }, module_class=Money))
    module_config = {
        "assets_ratios": {
            "test": 0.4,
            "test2": 0.1,
        },
    }
    default_manager.add_module(ModuleConfig(name="investing", module_config=module_config, module_class=Investing))
    default_manager.next_year()
    assert default_manager.total_assets == pytest.approx(1100)
    assert default_manager.get_module("test").money_value == pytest.approx(0.4 * 1100)
    assert default_manager.get_module("test2").money_value == pytest.approx(0.1 * 1100)
