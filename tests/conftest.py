import pytest
from fup.core.config import BluePrint
from fup.core.manager import Manager
from fup.core.module import AssetModule
from fup.core.functions import get_blueprint
import fup.profiles


@pytest.fixture(scope="function")
def default_config():
    return {
        "simulation": {
            "start_year": 2000,
            "end_year": 2020,
            "random": False,
        },
        "profile": {
            "class": "profiles.profiles.FullInvestment",
            "birth_year": 2000,
            "retirement_year": 2010,
        },
    }


@pytest.fixture(scope="function")
def modules_config(default_config):
    default_config["modules"] = {
        "Job": {
            "start_income": 42000,
            "prob_find_job": 0,
            "prob_lose_job": 0,
            "unemployed_months": 0,
            "class": "main.work.Job"
        },
        "main.investing.Investing": {
            "run_end_of_year": True,
            "assets_ratios": {
                "stocks": 0.4,
            },
        },
        "stocks": {"class": "assets.investment.Standard",
                   "start_money_value": 0,
                   "gains_tax": 0.25,
                   "exchange_fee": 0.0,
                   "depot_costs": 0.0,
                   "value_increase_mean": 0.1,
                   "value_increase_std": 0.1,
                   },
        "main.environment.Inflation": {
            "inflation_mean": 2.,
            "inflation_std": 2
        },
        "main.taxes.Taxes": {
            "tax_rates": [
                {"taxable_income": 0 + 9168, "tax_rate": 0.},
                {"taxable_income": 3000 + 9168, "tax_rate": 0.04},
                {"taxable_income": 8000 + 9168, "tax_rate": 0.1},
                {"taxable_income": 15000 + 9168, "tax_rate": 0.147},
                {"taxable_income": 26000 + 9168, "tax_rate": 0.20},
                {"taxable_income": 42000 + 9168, "tax_rate": 0.25},
                {"taxable_income": 64000 + 9168, "tax_rate": 0.303},
                {"taxable_income": 116000 + 9168, "tax_rate": 0.355},
                {"taxable_income": 325000 + 9168, "tax_rate": 0.405},
                {"taxable_income": 827000 + 9168, "tax_rate": 0.43}],
            "taxable_incomes": ["Job"],
            "tax_offsets": []
        },
        "CurrentAccount": {
            "class": "assets.bank.CurrentAccount",
            "run_end_of_year": True,
            "start_money_value": 1000,
            "penalty_interest_limit": 50000,
            "penalty_interest_rate": 0.05,
            "overdraft_rate": 0.0775,
        },
    }
    return default_config


@pytest.fixture(scope="function")
def default_profile_blueprint(default_config):
    return get_blueprint(config=default_config["profile"], root_module=fup.profiles)


@pytest.fixture(scope="function")
def default_manager(default_config, default_profile_blueprint):
    module_blueprints = [
        BluePrint(name="CurrentAccount", build_config={"start_money_value": 0}, build_class=AssetModule),
    ]
    return Manager(config=default_config, profile_blueprint=default_profile_blueprint,
                   current_account_name="CurrentAccount", module_blueprints=module_blueprints)
