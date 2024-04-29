# influence diffusion model
import networkx as nx

"""
    Create a random network with networkx using Erdos-Renyi model
    Input: 
        params: a dict of network parameters {n=n_value, p=p_value}, where n is the number of nodes, and p is the 
                probability of these nodes to connect with each other
    Output:
        graph: a generated random graph
"""


def generate_random_network(n, p):
    graph = nx.erdos_renyi_graph(n, p)
    return graph


if __name__ == '__main__':
    params = {'n': 20, 'p': 0.1}
    G = generate_random_network(**params)
    print(G.number_of_nodes())
    print(G.number_of_edges())
