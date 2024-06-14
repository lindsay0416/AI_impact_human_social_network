import networkx as nx
import pickle
import logging
import argparse
import json

logger = logging.getLogger("ds_tool")
logging.basicConfig(level="INFO")

def init_parser():
    parser = argparse.ArgumentParser(description="Hyper Parameters")
    parser.add_argument('-d', '--dataset', type=str, default='facebook')
    args = parser.parse_args()

    parser.print_help()
    return args

def convert_tool(dataset_file):
    G = nx.Graph()
    with open(f"input/{dataset_file}") as file:
        for line in file:
            # Split the line into two nodes
            node1, node2 = map(int, line.split())
            # Add an edge between the two nodes in the graph
            G.add_edge(node1, node2)
    save_graph(G, "graph.G")
    return G

# save a graph to file
def save_graph(graph, name):
    with open(f"saved/{name}", "wb") as f:
        pickle.dump(graph, f)
    logger.info(f"Saved to saved/{name}")


# load a saved graph from file
def load_graph(name):
    with open(f"saved/{name}", "rb") as f:
        G = pickle.load(f)
    logger.info(f"Load graph from saved/{name}")
    return G


def graph_show_info(G):
    logger.info(f"No. of edges: {len(list(G.edges()))}")
    logger.info(f"No. of nodes: {len(list(G.nodes()))}")

def graph_to_json(G):
    nodes = []
    for node in G.nodes():
        n = {"id": node,"uid": G.nodes()[node]["uid"], "profile": G.nodes()[node]["profile"]}
        nodes.append(n)
    
    data = {"nodes": nodes, "edges": list(G.edges())}
    with open('saved/graph.json', 'w') as f:
        json.dump(data, f, indent=4)
    logger.info(f"Graph information saves to saved/graph.json")
        

if __name__ == '__main__':
    args = init_parser()
    print("---------------------------------------")
    print(f"Dataset: {args.dataset}")
    print("---------------------------------------")

    convert_tool(args.dataset)
    G = load_graph("graph.G")
    graph_show_info(G)