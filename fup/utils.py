import inspect
import networkx as nx
from fup.core.manager import Manager
from fup.core.functions import get_full_name
import fup.modules


def get_module_list(config):
    module_list = [m for m in get_all_standard_modules() if get_full_name(m) in config["module_list"]]

    # dry run to get dependencies
    manager = Manager(config, module_list)
    manager.next_year()

    G = nx.DiGraph()
    G.add_node("root")

    # look up all dependencies
    print("## Dependencies  ##")
    for module_name in manager.modules:
        module = manager.modules[module_name]
        G.add_node(module_name)
        for dep_name in module.depends_on_modules:
            print(f"{dep_name} -> {module_name}")
            G.add_edge(dep_name, module_name)
        for modify_name in module.modifies_modules:
            print(f"{module_name} -> {modify_name}")
            G.add_edge(module_name, modify_name)

    # check for loop
    try:
        cycle = nx.find_cycle(G, orientation="original")
        raise Exception(f"Dependency loop found: {cycle}")
    except nx.NetworkXNoCycle:
        pass

        # add root dependencies
    for node in G.nodes():
        if node == "root":
            continue
        if len(G.in_edges(node)) < 1:
            G.add_edge("root", node)

    # Traverse Graph
    dep_checked_list = list(reversed(list(nx.dfs_postorder_nodes(G, source="root"))))[1:]

    sorted_modules = []
    for module_name in dep_checked_list:
        sorted_modules += [m for m in module_list if get_full_name(m) == module_name]

    return sorted_modules


def get_all_standard_modules(module=None, classes=None):
    if module is None:
        module = fup.modules
    if classes is None:
        classes = []
    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj) and "fup.modules" in str(obj):   # FIXME a little bit hacky...
                classes += [obj]
        if inspect.ismodule(obj) and "fup.modules" in obj.__name__:
            classes = get_all_standard_modules(module=obj, classes=classes)
    return classes
