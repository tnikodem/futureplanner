import time
import copy
import pandas as pd
import networkx as nx
from fup.core.config import ModuleConfig
from fup.core.manager import Manager
from fup.core.functions import get_module_config_list
from fup.profiles import profiles
import fup.modules


def get_sorted_module_config_list(config):
    # TODO put somewhere else, where??!
    # imports Manager -> no cyclic imports!
    module_list = get_module_config_list(config=config, root_module=fup.modules)

    # dry run to get dependencies
    manager = Manager(config, module_list, profile_class=profiles.Test)
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

    sorted_modules += get_module_config_list(config=config, root_module=fup.modules, end_of_year=True)

    return sorted_modules


def get_start_values(config, profile_class, monitoring_class=None):
    sorted_module_config_list = get_sorted_module_config_list(config=config)
    manager = fup.core.manager.Manager(config=config, module_list=sorted_module_config_list,
                                       profile_class=profile_class,
                                       monitoring_class=monitoring_class)
    manager.next_year()
    rows = []
    for module_name in manager.modules:
        rows += [manager.modules[module_name].info_dict()]
    return pd.DataFrame(rows)


def run_simulations(config, runs=100, profile_class=None, monitoring_class=None, debug=False):
    config = copy.deepcopy(config)

    time_start = time.time()

    module_list = get_sorted_module_config_list(config)

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
        print(f"Finished {runs} runs in {round(time_end - time_start, 2)}s")

    return df, df_stats
