import pytest
import random

from fup.core.config import ModuleConfig
from fup.core.manager import Manager

from fup.modules.assets.money import Money
from fup.modules.assets.investment import Standard


def test_money(default_config):
    manager = Manager(config=default_config, module_list=[])
    manager.add_module(
        ModuleConfig(name="assets.money.Money", module_config={"start_money_value": 500}, module_class=Money))
    manager.next_year()
    assert manager.df_row["money"] == pytest.approx(500)
    assert manager.total_assets == pytest.approx(500)


def test_standard(default_manager):
    default_manager.add_module(ModuleConfig(name="test", module_config={"start_money_value": 1000,
                                                                        "gains_tax": 0.25,
                                                                        "exchange_fee": 0.1,
                                                                        "depot_costs": 0.01,
                                                                        "value_increase_mean": 0.1,
                                                                        "value_increase_std": 0.04,
                                                                        "info_name": "test"
                                                                        }, module_class=Standard))
    default_manager.add_module(ModuleConfig(name="test2", module_config={"start_money_value": 0,
                                                                         "gains_tax": 0.25,
                                                                         "exchange_fee": 0.1,
                                                                         "depot_costs": 0.01,
                                                                         "value_increase_mean": 0.1,
                                                                         "value_increase_std": 0.04,
                                                                         }, module_class=Standard))
    default_manager.next_year()
    assert default_manager.df_row["test"] == pytest.approx(1000 * 1.1 * (1 - 0.01))
    assert default_manager.total_assets == pytest.approx((1000 + 100) * (1 - 0.01))
    # random
    random.seed(42)
    default_manager.config["simulation"]["random"] = True
    default_manager.next_year()
    assert default_manager.total_assets == pytest.approx(1179.70, 1e-5)
