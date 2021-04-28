import time
import copy
import inspect
import pandas as pd
import networkx as nx
from fup.core.manager import Manager, ModuleConfig
from fup.core.functions import get_full_class_name
import fup.modules


def get_module_list(config):
    config = copy.deepcopy(config)  # dict is "cleaned"

    standard_modules = get_all_standard_modules()
    module_list = list()
    for name in config["modules"].keys():
        module_config = config["modules"][name]
        if module_config is None:
            module_config = {}
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

    # dry run to get dependencies
    manager = Manager(config, module_list)
    manager.dependency_check()

    G = nx.DiGraph()
    G.add_node("root")

    # look up all dependencies
    for module_name in manager.modules:
        module = manager.modules[module_name]
        G.add_node(module_name)
        for dep_name in module.depends_on_modules:
            G.add_edge(dep_name, module_name)
        for modify_name in module.modifies_modules:
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
        sorted_modules += [m for m in module_list if m.name == module_name]

    # add end of year modules, without dep check
    for name in config["modules"].keys():
        module_config = config["modules"][name]
        if module_config is None:
            module_config = {}
        if "run_end_of_year" not in module_config or not module_config["run_end_of_year"]:
            continue
        del module_config["run_end_of_year"]
        if "class" in module_config:
            module_class = standard_modules[module_config["class"]]
            del module_config["class"]
        else:
            module_class = standard_modules[name]
        sorted_modules += [ModuleConfig(name=name,
                                        module_config=module_config,
                                        module_class=module_class
                                       )]

    return sorted_modules


def get_all_standard_modules(module=None, classes=None):
    if module is None:
        module = fup.modules
    if classes is None:
        classes = dict()
    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj) and "fup.modules" in str(obj):   # FIXME a little bit hacky...
            classes[get_full_class_name(obj)] = obj
        if inspect.ismodule(obj) and "fup.modules" in obj.__name__:
            classes = get_all_standard_modules(module=obj, classes=classes)
    return classes


def get_module_start_values(config, profile_class=None, monitoring_class=None):
    module_list = get_module_list(config)
    manager = fup.core.manager.Manager(config=config, module_list=module_list, profile_class=profile_class,
                                       monitoring_class=monitoring_class)
    manager.next_year()

    dicts = []
    for module_name in manager.modules:
        dicts += [manager.modules[module_name].info_dict()]
    df_mods = pd.DataFrame(dicts)

    return df_mods


def run_montecarlo(config, runs=100, profile_class=None, monitoring_class=None, debug=False):
    config = copy.deepcopy(config)

    time_start = time.time()

    module_list = get_module_list(config)

    dfs = []
    stats = []
    for i in range(runs):
        manager = fup.core.manager.Manager(config=config, module_list=module_list,
                                           profile_class=profile_class, monitoring_class=monitoring_class)

        df_rows = []
        for i_year in range(config["simulation"]["end_year"] - config["simulation"]["start_year"]):
            manager.next_year()
            df_rows += [manager.get_df_row()]
        df = pd.DataFrame(df_rows)

        df["run"] = i

        # tax correction
        df["expenses_net"] = df["expenses"] - df["tax"] - df["insurances"]
        df["income_net"] = df["income"] - df["tax"] - df["insurances"]
        # Inflation corrected
        df["expenses_net_cor"] = df["expenses_net"] / df["total_inflation"]
        df["income_net_cor"] = df["income_net"] / df["total_inflation"]
        df["assets_cor"] = df["assets"] / df["total_inflation"]

        dfs += [df]
        stats += [manager.get_stats()]

    df = pd.concat(dfs)
    df_stats = pd.DataFrame(stats)

    time_end = time.time()
    if debug:
        print(f"Finished {runs} runs in {round(time_end-time_start, 2)}s")

    return df, df_stats

