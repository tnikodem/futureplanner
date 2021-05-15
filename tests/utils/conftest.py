import pytest


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
        "assets.money.Money": {
            "start_money_value": 1000,
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
            "inflation_mean": 2.
        },
    }
    return default_config
