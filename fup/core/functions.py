
def get_full_class_name(module):
    module_name = module.__module__
    class_name = module.__name__

    # remove fup.modules from name
    if module_name[:4] == "fup.":
        module_name = module_name[4:]
        if module_name[:8] == "modules.":
            module_name = module_name[8:]

    return module_name+"."+class_name
