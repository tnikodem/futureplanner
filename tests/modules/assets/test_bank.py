import pytest

from fup.core.config import BluePrint
from fup.core.manager import Manager
from fup.modules.assets.bank import CurrentAccount


def test_current_account(default_config, default_profile_blueprint):
    module_blueprints = [
        BluePrint(name="CurrentAccount",
                  run_end_of_year=True,
                  build_class=CurrentAccount,
                  build_config={"class": "assets.bank.CurrentAccount",
                                "start_money_value": 1000,
                                "penalty_interest_limit": 50000,
                                "penalty_interest_rate": 0.05,
                                "overdraft_rate": 0.0775,
                                }),
    ]
    manager = Manager(config=default_config, profile_blueprint=default_profile_blueprint,
                      current_account_name="CurrentAccount", module_blueprints=module_blueprints)

    manager.next_year()
    assert manager.total_assets == pytest.approx(1000)

    # penalty interest
    manager.get_module("CurrentAccount").change(99000)
    manager.next_year()
    assert manager.total_assets == pytest.approx(100000 - 0.05 * 50000)

    # overdraft
    manager.get_module("CurrentAccount").money_value = -1000
    manager.next_year()
    assert manager.total_assets == pytest.approx(-(1000 + 0.0775 * 1000))
