from fup.core.functions import get_full_class_name


def test_get_full_class_name():
    class TestClass:
        pass
    class_name = get_full_class_name(TestClass)
    assert class_name.split(".")[-1] == "TestClass"
