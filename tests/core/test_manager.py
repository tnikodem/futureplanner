from fup.core.config import BluePrint
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


def test_manager_dependency(default_config, default_profile_blueprint):
    module_blueprints = [
        BluePrint(name="test3", build_config={}, build_class=Change3),
        BluePrint(name="test1", build_config={"value1": 1}, build_class=Change1),
        BluePrint(name="test2", build_config={"value2": 2}, build_class=Change2),
        BluePrint(name="CurrentAccount", build_config={"start_money_value": 1000}, build_class=AssetModule),
    ]
    manager = Manager(config=default_config,
                      module_blueprints=module_blueprints,
                      profile_blueprint=default_profile_blueprint,
                      current_account_name="CurrentAccount")
    # dependency check
    manager.dependency_check()
    assert manager.get_module("test2").depends_on_modules == {'test1'}
    assert manager.get_module("test3").modifies_modules == {'test1'}


def test_manager(default_config, default_profile_blueprint):
    # empty manager
    manager = Manager(config=default_config,
                      profile_blueprint=default_profile_blueprint,
                      current_account_name="CurrentAccount")
    assert manager is not None
    # manager with modules
    module_blueprints = [
        BluePrint(name="test3", build_config={}, build_class=Change3),
        BluePrint(name="test1", build_config={"value1": 1}, build_class=Change1),
        BluePrint(name="CurrentAccount", build_config={"start_money_value": 1000}, build_class=AssetModule),
    ]
    manager = Manager(config=default_config,
                      module_blueprints=module_blueprints,
                      profile_blueprint=default_profile_blueprint,
                      current_account_name="CurrentAccount")
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
