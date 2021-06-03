from fup.core.manager import Manager
from fup.profiles import profiles


def test_full_investment(default_config):
    manager = Manager(config=default_config, module_list=[], profile_class=profiles.FullInvestment)
    assert manager.profile.retired is False
    for i in range(10):
        manager.next_year()
    assert manager.profile.retired is True
