from fup.core.config import ModuleConfig
from fup.core.manager import Manager
from fup.core.module import ChangeModule, AssetModule


class Change1(ChangeModule):
    def next_year(self):
        self.value1 += 1
        self.expenses = self.value1


class Change2(ChangeModule):
    def next_year(self):
        value1 = self.get_prop("test1", "value1")
        self.expenses = value1


class Change3(ChangeModule):
    def next_year(self):
        change_value1 = self.get_prop_changer("test1", "value1")
        change_value1(2)
        self.income = 100


def test_manager_dependency(default_config):
    module_list = [
        ModuleConfig(name="test3", module_config={}, module_class=Change3),
        ModuleConfig(name="test1", module_config={"value1": 1}, module_class=Change1),
        ModuleConfig(name="test2", module_config={"value2": 2}, module_class=Change2),
        ModuleConfig(name="assets.money.Money", module_config={"start_money_value": 1000}, module_class=AssetModule),
    ]
    manager = Manager(config=default_config, module_list=module_list)
    # dependency check
    manager.dependency_check()
    assert manager.get_module("test2").depends_on_modules == {'test1'}
    assert manager.get_module("test3").modifies_modules == {'test1'}


def test_manager(default_config):
    # empty manager
    manager = Manager(config=default_config, module_list=[])
    assert manager is not None
    # manager with modules
    module_list = [
        ModuleConfig(name="test3", module_config={}, module_class=Change3),
        ModuleConfig(name="test1", module_config={"value1": 1}, module_class=Change1),
        ModuleConfig(name="assets.money.Money", module_config={"start_money_value": 1000}, module_class=AssetModule),
    ]
    manager = Manager(config=default_config, module_list=module_list)
    assert manager is not None
    assert manager.total_assets == 1000
    manager.next_year()
    df_row = manager.df_row
    assert df_row["year"] == 2001
    assert df_row["income"] == 100
    assert df_row["expenses"] == 3
    manager.next_year()
    df_row = manager.df_row
    assert df_row["year"] == 2002
    assert df_row["income"] == 100
    assert df_row["expenses"] == 7
