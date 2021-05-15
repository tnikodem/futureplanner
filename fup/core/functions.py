import copy
import inspect

from fup.core.config import ModuleConfig


def get_full_class_name(module):
    module_name = module.__module__
    class_name = module.__name__

    # remove fup.modules from name
    if module_name[:4] == "fup.":
        module_name = module_name[4:]
        if module_name[:8] == "modules.":
            module_name = module_name[8:]

    return module_name + "." + class_name


def get_all_modules(root_module, classes=None, module_name=None):
    if classes is None:
        classes = dict()

    if module_name is None:
        module_name = root_module.__name__

    for name, obj in inspect.getmembers(root_module):
        if inspect.isclass(obj) and obj.__module__.startswith(module_name):
            classes[get_full_class_name(obj)] = obj
        if inspect.ismodule(obj) and obj.__name__.startswith(module_name):
            get_all_modules(root_module=obj, classes=classes, module_name=module_name)

    return classes


def get_module_config_list(root_module, config, end_of_year=False):
    config = copy.deepcopy(config)  # FIXME, class and run_end_of_year is "cleaned"
    standard_modules = get_all_modules(root_module=root_module)

    module_list = []
    for name in config["modules"].keys():
        module_config = config["modules"][name]
        if module_config is None:
            module_config = {}

        if end_of_year:
            if "run_end_of_year" not in module_config or not module_config["run_end_of_year"]:
                continue
            del module_config["run_end_of_year"]
        else:
            if "run_end_of_year" in module_config and module_config["run_end_of_year"]:
                continue

        if "class" in module_config:
            module_class = standard_modules[module_config["class"]]
            del module_config["class"]
        else:
            module_class = standard_modules[name]
        module_list += [ModuleConfig(name=name,
                                     module_config=module_config,
                                     module_class=module_class
                                     )]
    return module_list
