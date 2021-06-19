import pytest
from fup.core.config import BluePrint
from fup.core.manager import Manager
from fup.core.module import Module, AssetModule, ChangeModule


def test_module(default_config, default_profile_blueprint):
    manager = Manager(config=default_config,
                      current_account_name="CurrentAccount",
                      profile_blueprint=default_profile_blueprint)

    # Setup
    # plain module
    manager.add_module(BluePrint(name="test", build_config={}, build_class=Module))
    assert type(manager.get_module("test")) == Module
    # Module with parameter
    manager.add_module(BluePrint(name="test2", build_config={"test_parm": 123}, build_class=Module))
    assert manager.get_module("test2").test_parm == 123

    # getter
    assert manager.get_module("test").get_prop("test2", "test_parm") == 123
    # setter
    change_test_param = manager.get_module("test").get_prop_multiplier("test2", "test_parm")
    change_test_param(2)
    assert manager.get_module("test2").test_parm == 246

    # info dict
    info = manager.get_module("test2").info
    assert info["name"] == "test2"
    assert info["class"] == "core.module.Module"
    assert info["info"] == ""


class Change1(ChangeModule):
    def next_year(self):
        self.income = 1000
        self.expenses = 500


class Change2(ChangeModule):
    def next_year(self):
        self.expenses = 100


def test_change_module(default_manager):
    manager = default_manager
    manager.add_module(BluePrint(name="test", build_config={}, build_class=Change1))
    cmod = manager.get_module("test")
    cmod.next_year_wrapper()
    assert manager.df_row["income"] == 1000
    assert manager.df_row["expenses"] == 500
    manager.add_module(BluePrint(name="test2", build_config={}, build_class=Change2))
    cmod2 = manager.get_module("test2")
    cmod2.next_year_wrapper()
    assert manager.df_row["income"] == 1000
    assert manager.df_row["expenses"] == 600

    # info
    info = cmod.info
    assert info["name"] == "test"
    assert info["class"] == "test_module.Change1"
    assert info["info"] == ""
    assert info["income"] == 1000
    assert info["expenses"] == 500


def test_assets_module(default_config, default_profile_blueprint):
    manager = Manager(config=default_config,
                      profile_blueprint=default_profile_blueprint,
                      current_account_name="CurrentAccount")

    gains_tax = 0.25
    exchange_fee = 0.1
    manager.add_module(BluePrint(name="test", build_config={"start_money_value": 1000,
                                                            "gains_tax": gains_tax,
                                                            "exchange_fee": exchange_fee
                                                            }, build_class=AssetModule))
    amod = manager.get_module("test")
    assert amod.money_value == 1000

    # invest money
    assert amod.change(money=500) == -500
    assert amod.money_value == 1450

    # year passed, item gained value
    amod.asset_value *= 2
    assert amod.money_value == 2900

    # change back into money
    value_with_fee = 2 * (1 - exchange_fee)
    assert amod.change(money=-500) == pytest.approx(
        (500 - (value_with_fee - 1) / value_with_fee * 500 * gains_tax) * (1 - exchange_fee))
    assert amod.money_value == 2400

    # year passed, item gained value
    amod.asset_value *= 3
    assert amod.money_value == 7200

    # invest money
    assert amod.change(money=8000) == -8000
    assert amod.money_value == 7200 + 7200

    # year passed, item gained value
    amod.asset_value *= 2
    assert amod.money_value == 28800

    # change back into money
    # half money with gain 12
    value_with_fee_1 = 12 * (1 - exchange_fee)
    # other half with gain 2
    value_with_fee_2 = 2 * (1 - exchange_fee)
    assert amod.change(money=-14400) == pytest.approx((14400. - (7200. * (value_with_fee_1 - 1) / value_with_fee_1 + 7200. * (value_with_fee_2 - 1) / value_with_fee_2) * gains_tax) * (1. - exchange_fee))
    assert amod.money_value == 14400

    # info dict
    info = amod.info
    assert info["name"] == "test"
    assert info["class"] == "core.module.AssetModule"
    assert info["info"] == ""
    assert info["value"] == 14400
