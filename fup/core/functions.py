import inspect


def get_full_class_name(module):
    module_name = module.__module__
    class_name = module.__name__

    # remove fup.modules from name
    if module_name[:4] == "fup.":
        module_name = module_name[4:]
        if module_name[:8] == "modules.":
            module_name = module_name[8:]

    return module_name + "." + class_name


def get_all_modules(module, classes=None, module_name=None):
    if classes is None:
        classes = dict()

    if module_name is None:
        module_name = module.__name__

    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj) and obj.__module__.startswith(module_name):
            classes[get_full_class_name(obj)] = obj
        if inspect.ismodule(obj) and obj.__name__.startswith(module_name):
            get_all_modules(module=obj, classes=classes, module_name=module_name)

    return classes
