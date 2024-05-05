# influence diffusion model
import os.path

import networkx as nx
import logging
import json

from model.agent import Agent
from model.environment import Environment, save_graph, load_graph

logger = logging.getLogger("influence_diffusion")
logging.basicConfig(level="INFO")

NODE_SIZE = 20
CONNECT_PROB = 0.1
IS_DIRECTED = True
TIMESTEP = 10
ROUND = 1
SEED_SET_SIZE = 1
INFLUENCE_PROB = 0.1


def start_diffusion(params):
    timestep = params.get("timestep")
    node_size = params.get("node_size")
    connect_prob = params.get("connect_prob")
    is_directed = params.get("is_directed")
    seed_set_size = params.get("seed_set_size")

    for step in range(0, timestep):
        if step == 0:
            # Initialize environment at timestep 0
            environment = Environment(node_size=node_size, connect_prob=connect_prob, is_directed=is_directed)
            # environment.select_seeds(seed_set_size)
            environment.select_fix_seeds([1])
            save_graph(environment.graph)

        for user in environment.graph.nodes():
            user_agent = environment.graph.nodes()[user]["data"]
            if user_agent.status == 1:
                user_agent.start_influence()

        calculate_coverage(environment, step)

def calculate_coverage(environment, timestep):
    influence_coverage = 0
    for node in environment.graph.nodes():
        if environment.graph.nodes[node]["data"].status == 1:
            influence_coverage += 1
    logger.info(f"Current timestep {timestep} -> No. of active users: {influence_coverage}")


def simulation(parameters):
    # extract parameters:
    no_of_rounds = parameters.get("round")

    for r in range(no_of_rounds):
        start_diffusion(parameters)
        # TODO - global analysis


def set_simulation_parameters():
    parameters = {
        "seed_set_size": SEED_SET_SIZE,
        "round": ROUND,
        "timestep": TIMESTEP,
        "influence_prob": INFLUENCE_PROB, # for test, we set a uniform probability
        "node_size": NODE_SIZE,
        "connect_prob": CONNECT_PROB,
        "is_directed": IS_DIRECTED
    }

    # save parameters to a json file
    with open("../saved/parameters.json", "w") as json_file:
        json.dump(parameters, json_file, indent=4)
        logger.info("parameters saved to ../saved/parameters.json")
    return parameters


if __name__ == '__main__':
    # set simulation parameters
    if not os.path.exists("../saved/parameters.json"):
        set_simulation_parameters()

    # load parameters
    with open("../saved/parameters.json", "r") as param_json:
        parameters = json.load(param_json)

    simulation(parameters)