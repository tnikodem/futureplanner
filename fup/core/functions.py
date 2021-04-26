

def get_full_class_name(module):
    return module.__module__[12:]+"."+module.__name__  # FIXME a little bit hacky, subtract fup.modules from module name
