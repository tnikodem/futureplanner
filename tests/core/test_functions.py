from fup.core.functions import get_full_class_name, get_all_modules, get_module_config_list


def test_get_full_class_name():
    class TestClass:
        pass

    class_name = get_full_class_name(TestClass)
    assert class_name.split(".")[-1] == "TestClass"


def test_get_all_modules():
    import fup.modules
    module_list = get_all_modules(root_module=fup.modules)
    assert "main.work.Job" in module_list.keys()
    assert "assets.money.Money" in module_list.keys()


def test_get_module_config_list():
    import fup.modules
    config = {
        "modules": {
            "main.environment.Inflation": {
                "inflation_mean": 2.2
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
    module_config_list = get_module_config_list(root_module=fup.modules, config=config)
    assert len(module_config_list) == 2
    assert module_config_list[0].name == "main.environment.Inflation"
    assert module_config_list[0].module_class == fup.modules.main.environment.Inflation
    assert module_config_list[0].module_config["inflation_mean"] == 2.2
    assert module_config_list[1].name == "Job"
    assert module_config_list[1].module_config == {"start_income": 42000}
    assert module_config_list[1].module_class == fup.modules.main.work.Job

    module_config_list = get_module_config_list(root_module=fup.modules, config=config, end_of_year=True)
    assert len(module_config_list) == 1
    assert module_config_list[0].name == "main.investing.Investing"
    assert module_config_list[0].module_class == fup.modules.main.investing.Investing
    assert module_config_list[0].module_config == {"assets_ratios": {"test": 0.4}}
