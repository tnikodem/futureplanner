import pytest
from fup.core.manager import Manager, ModuleConfig
from fup.core.module import Module, AssetModule, ChangeModule


def test_module(default_config):
    manager = Manager(config=default_config, module_list=[])

    # Setup
    # plain module
    manager.add_module(ModuleConfig(name="test", module_config={}, module_class=Module))
    assert type(manager.get_module("test")) == Module
    # Module with parameter
    manager.add_module(ModuleConfig(name="test2", module_config={"test_parm": 123}, module_class=Module))
    assert manager.get_module("test2").test_parm == 123

    # getter
    assert manager.get_module("test").get_prop("test2", "test_parm") == 123
    # setter
    change_test_param = manager.get_module("test").get_prop_changer("test2", "test_parm")
    change_test_param(2)
    assert manager.get_module("test2").test_parm == 246

    # info dict
    info_dict = manager.get_module("test2").info_dict()
    assert info_dict["name"] == "test2"
    assert info_dict["class"] == "core.module.Module"
    assert info_dict["info"] == ""


def test_change_module(default_config):
    manager = Manager(config=default_config, module_list=[])

    manager.add_module(ModuleConfig(name="test", module_config={}, module_class=ChangeModule))
    cmod = manager.get_module("test")
    cmod.expenses = 1000
    cmod.income = 2000
    cmod.calc_next_year()
    assert manager.income == 44000
    assert manager.expenses == 36000
    manager.add_module(ModuleConfig(name="test2", module_config={}, module_class=ChangeModule))
    cmod2 = manager.get_module("test2")
    cmod2.expenses = 3000
    cmod2.income = 4000
    cmod2.calc_next_year()
    assert manager.income == 48000
    assert manager.expenses == 39000

    # info dict
    info_dict = cmod.info_dict()
    assert info_dict["name"] == "test"
    assert info_dict["class"] == "core.module.ChangeModule"
    assert info_dict["info"] == ""
    assert info_dict["income"] == 2000
    assert info_dict["expenses"] == 1000


def test_assets_module(default_config):
    gains_tax = 0.25
    exchange_fee = 0.1

    manager = Manager(config=default_config, module_list=[])

    manager.add_module(ModuleConfig(name="test", module_config={"start_money_value": 1000,
                                                                "gains_tax": gains_tax,
                                                                "exchange_fee": exchange_fee
                                                                }, module_class=AssetModule))
    amod = manager.get_module("test")
    assert amod.money_value == 1000

    # invest money
    assert amod.change(money=500) == -500
    assert amod.money_value == 1450

    # year passed, item gained value
    amod.asset_value *= 2
    assert amod.money_value == 2900

    # change back into money
    assert amod.change(money=-500) == pytest.approx((500 - (2.-1.)/2. * 500 * gains_tax) * (1 - exchange_fee))
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
    # half money with gain 12 -> tax = 7200 * 11/12 * 0.25
    # other half with gain 2 -> tax = 7200 * 1/2 * 0.25
    assert amod.change(money=-14400) == pytest.approx(
        (14400. - (7200. * 11./12. + 7200. * 1./2.) * gains_tax) * (1. - exchange_fee))
    assert amod.money_value == 14400

    # info dict
    info_dict = amod.info_dict()
    assert info_dict["name"] == "test"
    assert info_dict["class"] == "core.module.AssetModule"
    assert info_dict["info"] == ""
    assert info_dict["value"] == 14400
