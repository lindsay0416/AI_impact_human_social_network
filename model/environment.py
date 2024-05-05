# init environment
import networkx as nx
import pickle
import logging
from model.agent import Agent
import os
import random

logger = logging.getLogger("environment")
logging.basicConfig(level="INFO")


class Environment:
    #  init a graph, graph can be None - so that a random graph would be created; or a Networkx graph.
    def __init__(self, graph=None, **kwargs):
        self.graph = graph
        for key, value in kwargs.items():
            setattr(self, key, value)
            if key == "node_size":
                self.node_size = value
            if key == "connect_prob":
                self.connect_prob = value
            if key == "is_directed":
                self.is_directed = value

        # init environment with random graph or a real-world social network
        if graph is None:
            logger.info("No graph data exists, creating a new graph...")
            if os.path.exists("../saved/G.pickle"):
                self.graph = load_graph()
            else:
                self.graph = generate_random_network(self.node_size, self.connect_prob, self.is_directed)
        else:
            # TODO
            self.graph = graph
            logger.info("Load a social network from dataset...")

        self.init_graph_data()

    """
        Initialize environment data, assign data to nodes
    """

    def init_graph_data(self):
        # assign user attributes to nodes, saved as an Agent object
        for node_id in self.graph.nodes:
            # init agent object
            node_data = Agent(node_id, self.graph)

            # assign in-neighbor and out-neighbor lists:
            # both are a list of integers, denotes userID of the adjacent users.
            node_data.in_neighbors = list(self.graph.predecessors(node_id))
            node_data.out_neighbors = list(self.graph.successors(node_id))

            # assign user data to node
            self.graph.nodes[node_id]['data'] = node_data

        logger.info("Initialize environment data")

    """
        Seed selection: here we use random selection
        - given a seed set size, randomly select initialized user agents as seeds.
    """
    def select_seeds(self, seedSetSize):
        seedSet = {}
        if seedSetSize > max(self.graph.nodes()):
            logger.error("Exceeds max value of node size")
            return
        while len(seedSet) < seedSetSize:
            try:
                selected = random.randint(min(self.graph.nodes()), max(self.graph.nodes()))
                if self.graph.nodes[selected]["data"].status == 0:
                    self.graph.nodes[selected]["data"].status = 1
                    seedSet[selected] = self.graph.nodes[selected]["data"]
            except ValueError as e:
                logger.error(f"An error occurred {e}, failed to assign user {selected} as seed")
        logger.info(f"Seed set: {list(seedSet.keys())}")


    """
            Seed selection: selected seed based on userID with a given int list
    """
    def select_fix_seeds(self, seedSet):
        for seed in seedSet:
            self.graph.nodes[seed]["data"].status = 1
        logger.info(f"Seed set: {seedSet}")

"""
    Create a random network with networkx using Erdos-Renyi model
    Input: 
        params: a dict of network parameters {n=n_value, p=p_value, is_directed=boolean_value}, 
        where n is the number of nodes, and p is the probability of these nodes to connect with each other, 
        is_directed suggests whether the graph is directed.
    Output:
        graph: a generated random graph
"""


def generate_random_network(n, p, is_directed):
    graph = nx.erdos_renyi_graph(n, p, directed=is_directed)
    save_graph(graph)
    return graph


# save a graph to file
def save_graph(graph):
    with open("../saved/G.pickle", "wb") as f:
        pickle.dump(graph, f)
    logger.info("Saved to ../saved/G.pickle")


# load a saved graph from file
def load_graph():
    with open("../saved/G.pickle", "rb") as f:
        G = pickle.load(f)
    logger.info("Load graph from ../saved/G.pickle")
    return G