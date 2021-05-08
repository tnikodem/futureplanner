from fup.core.functions import get_full_class_name, get_all_modules


def test_get_full_class_name():
    class TestClass:
        pass
    class_name = get_full_class_name(TestClass)
    assert class_name.split(".")[-1] == "TestClass"


def test_get_all_modules():
    import fup.modules
    module_list = get_all_modules(fup.modules)
    assert "main.work.Job" in module_list.keys()
    assert "assets.money.Money" in module_list.keys()
