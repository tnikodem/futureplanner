import random
import pytest

from fup.core.config import BluePrint
from fup.modules.main.environment import Inflation
from fup.modules.main.work import Job


def test_taxes(default_manager):
    inflation_build_config = {"inflation_mean": 2, "inflation_std": 0}
    default_manager.add_module(BluePrint(name="main.environment.Inflation", build_config=inflation_build_config,
                                            build_class=Inflation))
    job_build_config = {
        "start_income": 30000,
        "unemployed_months": 0,
        "prob_lose_job": 1.0,  # per month
        "prob_find_job": 0.0,  # per month
    }
    default_manager.add_module(BluePrint(name="Job", build_config=job_build_config, build_class=Job))
    default_manager.next_year()
    assert default_manager.df_row["income"] == pytest.approx(30000 * 1.02)

    default_manager.config["simulation"]["random"] = True
    random.seed(42)
    default_manager.next_year()
    assert default_manager.get_module("Job").unemployed_months == 12
    assert default_manager.get_module("Job").unemployed_months_this_year == 12
    assert default_manager.df_row["income"] == pytest.approx(0)

    # FIXME highly unstable test with several random numbers!
    random.seed(42)
    default_manager.get_module("Job").prob_find_job = 0.1
    default_manager.get_module("Job").prob_lose_job = 0
    default_manager.next_year()
    assert default_manager.get_module("Job").unemployed_months_this_year == 5
    assert default_manager.get_module("Job").unemployed_months == 0
    assert default_manager.df_row["income"] == pytest.approx(1.02 ** 3 * 30000 * (12 - 5) / 12)

    # TODO No Money when retired ?! part time Job??!
    default_manager.profile.retired = True
    default_manager.next_year()
    assert default_manager.df_row["income"] == pytest.approx(0)
