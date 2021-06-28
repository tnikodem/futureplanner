from fup.core.functions import get_full_class_name, get_all_modules, get_module_blueprints


def test_get_full_class_name():
    class TestClass:
        pass

    class_name = get_full_class_name(TestClass)
    assert class_name.split(".")[-1] == "TestClass"


def test_get_all_modules():
    import fup.modules
    module_list = get_all_modules(root_module=fup.modules)
    assert "main.work.Job" in module_list.keys()
    assert "assets.bank.CurrentAccount" in module_list.keys()


def test_get_module_config_list():
    import fup.modules
    config = {
        "modules": {
            "main.environment.Inflation": {
                "inflation_mean": 1.022
            },
            "Job": {
                "start_income": 42000,
                "class": "main.work.Job"
            },
            "main.investing.Investing": {
                "run_end_of_year": True,
                "assets_ratios": {
                    "test": 0.4,
                },
            }
        }
    }
    module_config_list = get_module_blueprints(root_module=fup.modules, config=config)
    assert len(module_config_list) == 3
    assert module_config_list[0].name == "main.environment.Inflation"
    assert module_config_list[0].build_class == fup.modules.main.environment.Inflation
    assert module_config_list[0].build_config["inflation_mean"] == 1.022

    assert module_config_list[1].name == "Job"
    assert module_config_list[1].build_config == {"start_income": 42000}
    assert module_config_list[1].build_class == fup.modules.main.work.Job

    assert module_config_list[2].name == "main.investing.Investing"
    assert module_config_list[2].build_class == fup.modules.main.investing.Investing
    assert module_config_list[2].build_config == {"assets_ratios": {"test": 0.4}}
    assert module_config_list[2].run_end_of_year is True
