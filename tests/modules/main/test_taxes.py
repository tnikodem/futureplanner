import pytest

from fup.core.config import ModuleConfig

from fup.core.module import Module
from fup.modules.main.environment import Inflation
from fup.modules.main.taxes import Taxes

inflation_module_config = {"inflation_mean": 0, "inflation_std": 1}
tax_module_config = {
    "tax_free_limit": 10000,
    "max_tax_increase_limit": 100000,
    "min_tax_rate": 0.1,
    "max_tax_rate": 0.4,
    "taxable_incomes": ["Job"],
    "tax_offsets": ["Health"]
}


def test_taxes(default_manager):
    default_manager.add_module(ModuleConfig(name="main.environment.Inflation", module_config=inflation_module_config,
                                            module_class=Inflation))
    default_manager.add_module(ModuleConfig(name="Job", module_config={"income": 30000}, module_class=Module))
    default_manager.add_module(ModuleConfig(name="Health", module_config={"expenses": 10000}, module_class=Module))
    default_manager.add_module(ModuleConfig(name="Tax", module_config=tax_module_config, module_class=Taxes))
    default_manager.next_year()
    assert default_manager.df_row["tax"] == pytest.approx(1333.333)  # TODO compare with reality


def test_no_taxes(default_manager):
    default_manager.add_module(ModuleConfig(name="main.environment.Inflation", module_config=inflation_module_config,
                                            module_class=Inflation))
    default_manager.add_module(ModuleConfig(name="Job", module_config={"income": 10000}, module_class=Module))
    default_manager.add_module(ModuleConfig(name="Health", module_config={"expenses": 0}, module_class=Module))
    default_manager.add_module(ModuleConfig(name="Tax", module_config=tax_module_config, module_class=Taxes))
    default_manager.next_year()
    assert default_manager.df_row["tax"] == pytest.approx(0)


def test_max_taxes(default_manager):
    default_manager.add_module(
        ModuleConfig(name="main.environment.Inflation", module_config=inflation_module_config,
                     module_class=Inflation))
    default_manager.add_module(ModuleConfig(name="Job", module_config={"income": 210000}, module_class=Module))
    default_manager.add_module(ModuleConfig(name="Health", module_config={"expenses": 0}, module_class=Module))
    default_manager.add_module(ModuleConfig(name="Tax", module_config=tax_module_config, module_class=Taxes))
    default_manager.next_year()
    assert default_manager.df_row["tax"] == pytest.approx(200000 * 0.4)
