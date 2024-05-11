import networkx as nx
import pickle
import logging
import argparse

logger = logging.getLogger("tool")
logging.basicConfig(level="INFO")

def init_parser():
    parser = argparse.ArgumentParser(description="Hyper Parameters")
    parser.add_argument('-d', '--dataset', type=str, default='facebook')
    args = parser.parse_args()

    parser.print_help()
    return args

def convert_tool(dataset_file):
    G = nx.Graph()
    with open(f"../input/{dataset_file}") as file:
        for line in file:
            # Split the line into two nodes
            node1, node2 = map(int, line.split())
            # Add an edge between the two nodes in the graph
            G.add_edge(node1, node2)
    save_graph(G)
    return G

# save a graph to file
def save_graph(graph):
    with open("../saved/G.pickle", "wb") as f:
        pickle.dump(graph, f)
    logger.info("Saved to saved/G.pickle")


# load a saved graph from file
def load_graph():
    with open("../saved/G.pickle", "rb") as f:
        G = pickle.load(f)
    logger.info("Load graph from saved/G.pickle")
    return G


def graph_show_info(G):
    logger.info(f"No. of edges:, {len(list(G.edges()))}")
    logger.info(f"No. of nodes:, {len(list(G.nodes()))}")


if __name__ == '__main__':
    args = init_parser()
    print("---------------------------------------")
    print(f"Dataset: {args.dataset}")
    print("---------------------------------------")

    convert_tool(args.dataset)
    G = load_graph()
    graph_show_info(G)