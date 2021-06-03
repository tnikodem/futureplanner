import time
import copy
import pandas as pd
import networkx as nx
from fup.core.config import BluePrint
from fup.core.manager import Manager
from fup.core.functions import get_module_blueprints, get_blueprint
import fup.profiles
import fup.modules


# TODO put this method somewhere else, where??!
def get_sorted_module_blueprints(config):
    # imports Manager -> no cyclic imports!
    module_blueprints = get_module_blueprints(config=config, root_module=fup.modules)
    profile_blueprint = get_blueprint(config=config["profile"], root_module=fup.profiles)

    # dry run to get dependencies
    manager = Manager(config,
                      module_blueprints=module_blueprints,
                      profile_blueprint=profile_blueprint,
                      current_account_name="CurrentAccount")

    manager.dependency_check()
    G = nx.DiGraph()
    G.add_node("root")
    # look up all dependencies
    for module_name, module in manager.modules.items():
        if module.run_end_of_year:
            continue
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
        sorted_modules += [m for m in module_blueprints if m.name == module_name]

    for module_name, module in manager.modules.items():
        if module.run_end_of_year:
            sorted_modules += [m for m in module_blueprints if m.name == module_name]

    return sorted_modules


def get_start_values(config):
    config = copy.deepcopy(config)
    config["simulation"]["random"] = False
    config["modules"]["main.environment.Inflation"]["inflation_mean"] = 0

    sorted_module_blueprints = get_sorted_module_blueprints(config=config)
    profile_blueprint = get_blueprint(config=config["profile"], root_module=fup.profiles)
    manager = fup.core.manager.Manager(config=config,
                                       module_blueprints=sorted_module_blueprints,
                                       profile_blueprint=profile_blueprint,
                                       current_account_name="CurrentAccount")
    manager.next_year()
    rows = []
    for module_name in manager.modules:
        rows += [manager.modules[module_name].info]
    return pd.DataFrame(rows)


def run_simulations(config, runs=100, debug=False):
    time_start = time.time()

    sorted_module_blueprints = get_sorted_module_blueprints(config)
    profile_blueprint = get_blueprint(config=config["profile"], root_module=fup.profiles)
    dfs = []
    stats = []
    for i in range(runs):
        manager = fup.core.manager.Manager(config=config,
                                           module_blueprints=sorted_module_blueprints,
                                           profile_blueprint=profile_blueprint,
                                           current_account_name="CurrentAccount")

        rows = []
        for i_year in range(config["simulation"]["end_year"] - config["simulation"]["start_year"]):
            manager.next_year()
            rows += [manager.df_row]
        df = pd.DataFrame(rows)
        df["run"] = i

        # tax correction
        df["expenses_net"] = df["expenses"] - df["tax"] - df["tax_offset"]
        df["income_net"] = df["income"] - df["tax"] - df["tax_offset"]
        # Inflation corrected
        df["expenses_net_cor"] = df["expenses_net"] / df["total_inflation"]
        df["income_net_cor"] = df["income_net"] / df["total_inflation"]
        df["assets_cor"] = df["assets"] / df["total_inflation"]

        dfs += [df]
        # TODO implement me stats += [manager.get_stats()]

    df = pd.concat(dfs)
    df_stats = pd.DataFrame(stats)

    if debug:
        print(f"Finished {runs} runs in {round(time.time() - time_start, 2)}s")

    return df, df_stats
