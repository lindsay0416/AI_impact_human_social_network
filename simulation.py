# entry of simulation
import os
import networkx as nx
import logging
import json

from model.agent import Agent
from model.environment import Environment
import tool.dataset_tool as dt

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
    # extract parameters:
    no_of_rounds = params.get("round")
    for r in range(no_of_rounds):
        logger.info(f"Round {r}")
        pass


def start_diffusion(params):
    timestep = params.get("timestep")
    node_size = params.get("node_size")
    connect_prob = params.get("connect_prob")
    is_directed = params.get("is_directed")
    is_external_dataset = params.get("is_external_dataset")

    round = params.get("round")


if __name__ == '__main__':
    if not os.path.exists("input/parameters.json"):
        parameters = set_simulation_params()
    else:
        # load parameters
        with open("input/parameters.json", "r") as param_json:
            parameters = json.load(param_json)

    simulation(parameters)
