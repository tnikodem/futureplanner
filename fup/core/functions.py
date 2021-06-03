import copy
import inspect

from fup.core.config import BluePrint


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


def get_blueprint(config, root_module):
    config = copy.deepcopy(config)
    assert "class" in config
    all_module_classes = get_all_modules(root_module=root_module)
    assert config["class"] in all_module_classes, all_module_classes
    build_class = all_module_classes[config["class"]]
    del config["class"]

    return BluePrint(build_class=build_class, build_config=config)


def get_module_blueprints(root_module, config):
    config = copy.deepcopy(config)  # FIXME, class and run_end_of_year is "cleaned"
    standard_modules = get_all_modules(root_module=root_module)

    blueprint_list = list()
    for name in config["modules"].keys():
        build_config = config["modules"][name]
        if build_config is None:
            build_config = dict()

        run_end_of_year = False
        if "run_end_of_year" in build_config:
            run_end_of_year = build_config["run_end_of_year"]
            del build_config["run_end_of_year"]

        if "class" in build_config:
            build_class = standard_modules[build_config["class"]]
            del build_config["class"]
        else:
            build_class = standard_modules[name]

        blueprint_list += [BluePrint(name=name,
                                     run_end_of_year=run_end_of_year,
                                     build_config=build_config,
                                     build_class=build_class)]
    return blueprint_list
