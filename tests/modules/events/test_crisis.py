import pytest
import random

from fup.core.config import ModuleConfig
from fup.core.manager import Manager

from fup.modules.assets.money import Money
from fup.modules.assets.investment import Standard


def test_oil_crisis_1973(default_manager):
    manager = default_manager

    # TODO first test dependend modules
