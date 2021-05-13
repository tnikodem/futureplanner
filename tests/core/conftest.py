import pytest


@pytest.fixture(scope="session")
def default_config():
    return {
        "simulation": {
            "start_year": 2000,
            "end_year": 2100,
            "start_income": 42000,
            "start_expenses": 35000,
        },
        "profile": {
            "retirement_year": 2050,
            "retirement_factor": 1,
        }
    }
