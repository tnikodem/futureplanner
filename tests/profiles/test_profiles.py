from fup.core.manager import Manager
from fup.core.functions import get_blueprint
import fup.profiles


def test_full_investment():
    config = {
        "simulation": {
            "start_year": 2000,
            "end_year": 2020,
            "random": False,
        },
        "profile": {
            "class": "profiles.profiles.FullInvestment",
            "birth_year": 2000,
            "retirement_year": 2010,
        }
    }

    profile_blueprint = get_blueprint(config=config["profile"], root_module=fup.profiles)

    manager = Manager(config=config, profile_blueprint=profile_blueprint, current_account_name="CurrentAccount")
    assert manager.profile.retired is False
    for i in range(10):
        manager.next_year()
    assert manager.profile.retired is True
