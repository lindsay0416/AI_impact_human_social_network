# entry of simulation
import os
import networkx as nx
from networkx.readwrite import json_graph
import logging
import json
from model.agent import Agent
from model.environment import Environment
import tool.dataset_tool as dt

from datetime import datetime
import time
import sys

# init logger
logger = logging.getLogger("simulation")
logging.basicConfig(level=logging.INFO)


NODE_SIZE = 20
CONNECT_PROB = 0.1
IS_DIRECTED = True
TIMESTEP = 10
ROUND = 1
INFLUENCE_PROB = 0.1,
BROADCASTING_PROB = 0.1,
INITIAL_MESSAGE = "This is an example initial message."


def set_simulation_params():
    parameters = {
        "round": ROUND,
        "timestep": TIMESTEP,
        "influence_prob": INFLUENCE_PROB,  # for test, we set a uniform probability
        "node_size": NODE_SIZE,
        "connect_prob": CONNECT_PROB,
        "is_directed": IS_DIRECTED,
        "broadcasting_prob": 0.1,
        "initial_message": INITIAL_MESSAGE
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
    random_edge = params.get("random_edges")
    is_directed = params.get("is_directed")
    is_external_dataset = params.get("is_external_dataset")
    initial_message = params.get("initial_message")
    generate_user_profile = params.get("generate_user_profile")
    broadcasting_prob = params.get("broadcasting_prob")
    location = params.get("location")
    
    if generate_user_profile:
        user_profile_prompt = params.get("user_profile_prompt")
        if location is None:
            user_profile_prompt = "Location of these users are random. Ages of these users follow Gaussian distribution, gender is half and half." +\
                                   user_profile_prompt 
        else:
            with open("input/context.json", 'r') as file:
                context = json.load(file)
            if context.get(location) is not None:
                population = "Population follows these distribution rules: " + json.dumps(context.get(location)) + "\n"
            else:
                population = ""
            user_profile_prompt = f"Location of these users are in {location}. \n" +\
                                    population + user_profile_prompt                                
        dt.generate_user_profile(user_profile_prompt, node_size)

    
    if not is_external_dataset:
        environment = Environment(
            node_size=node_size, 
            is_directed=is_directed,
            connect_prob=connect_prob, 
            random_edge=random_edge, 
            initial_message=initial_message
            )
    else:
        G = dt.load_graph("graph.G")
        dt.graph_show_info(G)
        environment = Environment(
            graph=G, 
            is_directed=is_directed,
            initial_message=initial_message)
        
    logger.info("Simulation initialization finished, start broadcasting...")
    initial_message_content = params.get("initial_message")
    environment.start_infection(broadcasting_prob, initial_message_content)

    logger.info(f"Seed selection finished, Seed Set: {str(environment.seedSet)}")
    dt.graph_to_json(environment.graph)
    dt.save_graph(environment.graph, "graph.G")

    # start diffusion
    no_of_rounds = params.get("round")

    rounds = []
    for r in range(no_of_rounds):
        round = {}
        result = start_diffusion(params, r, environment)
        reset_status(environment)
        round["round"] = r
        round["result"] = result
        rounds.append(round)

        # logger info
        logger.info(f" ======= Round {r} with Seed Set: {environment.seedSet} Finished ======= ")
    
    return rounds  

"""
    Reset status at the end of a round. This includes: clean up user agents' repositories, set up status to inactive (0).
"""
def reset_status(environment):
    for user in environment.graph.nodes():
        user_agent = environment.graph.nodes()[user]["data"]
        if user not in environment.seedSet:
            user_agent.update_status(0)
        user_agent.posts = []
        user_agent.repository = []
        if user in environment.seedSet:
            user_agent.set_as_seed(environment.initial_message)

def start_diffusion(params, round, environment):
    timestep = params.get("timestep")
    influence_prob = params.get("influence_prob")
    evolution_prob = params.get("evolution_prob")

    steps = []
    all_activated = []

    # print([environment.graph.nodes()[user]["data"].posts[0].content for user in environment.seedSet])
    for step in range(0, timestep):
        #  diffusion process:
        # at each timestep t, a set of active users start influence diffusion with an influence probability so that to influence their inactive neighbours
        # once the neighbors are influenced, they are recognized as newly activated nodes, and start influence diffusion at the next time step
        if step == 0:
            newly_activated = environment.seedSet
            data, user_data = global_analysis(environment, 0)
            step_result = {}
            step_result["step"] = 0
            step_result["data"] = data
            step_result["user_data"] = user_data
            steps.append(step_result)
            all_activated += newly_activated
        else:
            new_influenced = []
            for user in newly_activated:
                user_agent = environment.graph.nodes()[user]["data"]
                influenced = user_agent.start_influence(step, influence_prob)
                new_influenced += influenced
            
            # active user opinion evolution
            for au in all_activated:
                active_agent = environment.graph.nodes()[au]["data"]
                if au not in newly_activated:
                    active_agent.evolve(step, evolution_prob)

            step_result = {}
            step_result["step"] = step
            data, user_data = global_analysis(environment, step)
            step_result["data"] = data
            step_result["user_data"] = user_data
            steps.append(step_result)

            newly_activated = new_influenced
            all_activated += newly_activated
        with open("saved/simulation_result.json", 'w') as file:
            json.dump(step_result, file)
    
    return steps

def global_analysis(environment, timestep):
    coverage = calculate_coverage(environment, timestep)
    data = {"coverage": coverage}

    graph = environment.graph
    user_data = []
    for user in graph.nodes():
        ud = environment.graph.nodes()[user]["data"].to_dict()
        user_data.append(ud)

    return data, user_data

def calculate_coverage(environment, timestep):
    influence_coverage = 0
    for node in environment.graph.nodes():
        if environment.graph.nodes[node]["data"].status == 1:
            influence_coverage += 1
    logger.info(f"Current timestep {timestep} -> No. of active users: {influence_coverage}")
    return influence_coverage

if __name__ == '__main__':
    # init input and saved folders
    if not os.path.exists("input"):
        os.makedirs("input", exist_ok=True)
    if not os.path.exists("saved"):
        os.makedirs("saved", exist_ok=True)
    start_time = datetime.now().strftime('%Y%m%d%H%M%S')

    if not os.path.exists("input/parameters.json"):
        parameters = set_simulation_params()
    else:
        # load parameters
        with open("input/parameters.json", "r") as param_json:
            parameters = json.load(param_json)
    with open("saved/results.txt", 'w') as file:
        file.write('')

    # start simulation
    data = simulation(parameters)

    end_time = datetime.now().strftime('%Y%m%d%H%M%S')

    # ====== save simulation result to JSON file ====== 
    results = {}
    # add simulation metadata
    results["id"] = start_time
    results["start"] = start_time
    results["end"] = end_time
    results["simulation"] = data
    
    with open('saved/results.json', 'w') as f:
        json.dump(results, f, indent=4, separators=(',', ':'))