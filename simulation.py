# entry of simulation
import os
import networkx as nx
from networkx.readwrite import json_graph
import logging
import json

from model.agent import Agent
from model.environment import Environment
import tool.dataset_tool as dt

import time

# init logger
logger = logging.getLogger("simulation")
logging.basicConfig(level="INFO")

NODE_SIZE = 20
CONNECT_PROB = 0.1
IS_DIRECTED = True
TIMESTEP = 10
ROUND = 1
SEED_SET_SIZE = 1
INFLUENCE_PROB = 0.1


def set_simulation_params():
    parameters = {
        "seed_set_size": SEED_SET_SIZE,
        "round": ROUND,
        "timestep": TIMESTEP,
        "influence_prob": INFLUENCE_PROB,  # for test, we set a uniform probability
        "node_size": NODE_SIZE,
        "connect_prob": CONNECT_PROB,
        "is_directed": IS_DIRECTED
    }

    # save parameters to a json file
    with open("input/parameters.json", "w") as json_file:
        json.dump(parameters, json_file, indent=4)
        logger.info("parameters saved to saved/parameters.json")
    return parameters


def simulation(params):
    # init graph
    node_size = params.get("node_size")
    connect_prob = params.get("connect_prob")
    is_directed = params.get("is_directed")
    is_external_dataset = params.get("is_external_dataset")
    if not is_external_dataset:
        environment = Environment(node_size=node_size, connect_prob=connect_prob, is_directed=is_directed)
    else:
        G = dt.load_graph("graph.G")
        dt.graph_show_info(G)
        environment = Environment(graph=G, is_directed=is_directed)

    # start diffusion
    no_of_rounds = params.get("round")

    results = {}

    for r in range(no_of_rounds):
        logger.info(f"Round {r}")
        results[str(r)] = start_diffusion(params, r, environment)
        reset_status(environment)

        
    # TODO - save result
    with open('saved/results.json', 'w') as f:
        json.dump(results, f, indent=4)

"""
    Reset status at the end of a round. This includes: clean up user agents' repositories, set up status to inactive (0).
"""
def reset_status(environment):
    for user in environment.graph.nodes():
        user_agent = environment.graph.nodes()[user]["data"]
        user_agent.update_status(0)
        user_agent.posts = []
        user_agent.repository = []


def start_diffusion(params, round, environment):
    timestep = params.get("timestep")
    round = params.get("round")
    results = {}

    # set seedSet
    seed_set_size = params.get("seed_set_size")
    if seed_set_size is not None:
        environment.select_seeds(seed_set_size)
    elif params.get("seed_set") is not None:
        seed_set = json.loads(params.get("seed_set"))
        environment.select_fix_seeds(seed_set)
    else:
        environment.select_fix_seeds([min(environment.graph.nodes)])

    if round == 0:
        dt.save_graph(environment.graph, "graph.G")

    results[str(0)] = global_analysis(environment, 0)
    for step in range(1, timestep):
        for user in environment.graph.nodes():
            user_agent = environment.graph.nodes()[user]["data"]
            if user_agent.status == 1:
                user_agent.start_influence(step)
        data = global_analysis(environment, step)
        results[str(step)] = data
    return results

def global_analysis(environment, timestep):
    coverage = calculate_coverage(environment, timestep)
    # TODO: save global analysis result into elastic search. Here, as a test, we save it into JSON file. Currently only provide coverage analysis data
    data = {"data":{"coverage": coverage}}
    # graph_data = {'step': timestep, 'data': json_graph.node_link_data(environment.graph)}

    return data

def calculate_coverage(environment, timestep):
    influence_coverage = 0
    for node in environment.graph.nodes():
        if environment.graph.nodes[node]["data"].status == 1:
            influence_coverage += 1
    return f"Current timestep {timestep} -> No. of active users: {influence_coverage}"


if __name__ == '__main__':
    if not os.path.exists("input/parameters.json"):
        parameters = set_simulation_params()
    else:
        # load parameters
        with open("input/parameters.json", "r") as param_json:
            parameters = json.load(param_json)

    # start simulation
    simulation(parameters)
