import networkx as nx
import pickle
import logging
import argparse
import json
import matplotlib.pyplot as plt
import collections
import numpy as np
import re
import time

import openai
from tool.config_manager import ConfigManager
from analysis.result_analysis import json_formatter
from llm_generate_text import GenerateText

logger = logging.getLogger("ds_tool")
logging.basicConfig(level="INFO")
BATCH_SIZE = 30

def init_parser():
    parser = argparse.ArgumentParser(description="Hyper Parameters")
    parser.add_argument('-d', '--dataset', type=str, default='facebook')
    args = parser.parse_args()

    parser.print_help()
    return args

def generate_user_profile(prompt, node_size):
    profiles = ""
    batch_size = BATCH_SIZE
    batch_num = (node_size + batch_size - 1) // batch_size # 30 users as a batch
    for i in range(batch_num):
        generate_prompt = f"Generate user profiles for {batch_size} users as a 30-word unique description," +\
                          prompt
        print(generate_prompt)
        config_manager = ConfigManager('config.ini')
        api_key = config_manager.get_api_key()
        openai.api_key = api_key
        response, generate_prompt = GenerateText.get_generated_text(openai, generate_prompt)
        profiles += response

    with open("input/user_profile.txt", "w") as file:
        file.write(profiles)
    
    validate_generated_profile(prompt, node_size, batch_size)

def validate_generated_profile(prompt, node_size, batch_size):
    profiles = {}
    with open("input/user_profile.txt", "r") as file:
        data = file.read()

    profiles = {}
    matches = re.findall(r'\{(.*?)\}', data)
    for idx, entry in enumerate(matches, start=1):
        profileID = f"N{idx}"
        profile = {}
        if entry.strip():
            entry_data = entry.split("; ")
            for item in entry_data:
                key, value = item.split(": ", 1)
                profile[key] = value
        profiles[profileID] = profile

    profiles = {key: value for index, (key, value) in enumerate(profiles.items()) if index < node_size}
    json_data = json.dumps(profiles, indent=4)

    with open("input/user_profile.json", "w") as json_file:
        json_file.write(json_data)

    

def convert_tool(dataset_file):
    G = nx.Graph()
    with open(f"input/{dataset_file}") as file:
        for line in file:
            # Split the line into two nodes
            node1, node2 = map(int, line.split())
            # Add an edge between the two nodes in the graph
            G.add_edge(node1, node2)

    node_mapping = {node: new_id for new_id, node in enumerate(G.nodes())}
    G = nx.relabel_nodes(G, node_mapping)
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
        

def graph_to_figure(G):
    # Draw the network with customized nodes and edges
    plt.figure(figsize=(8, 8))  # Set the figure size
    pos = nx.spring_layout(G, seed=42)  # For consistent layout

    # Draw nodes and edges separately
    nx.draw_networkx_nodes(G, pos, node_size=700, node_color='lightblue')
    nx.draw_networkx_edges(G, pos, alpha=0.5, edge_color='gray')
    nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')

    plt.show()


def graph_degree_to_figure(G):
    degree_sequence = sorted([d for n, d in G.degree()], reverse=True)  # degree sequence
    # Count the number of nodes that have each degree
    degree_count = collections.Counter(degree_sequence)
    deg, cnt = zip(*degree_count.items())

    plt.figure(figsize=(10, 6))
    plt.bar(deg, cnt, width=0.80, color='b')

    plt.title("Degree Distribution")
    plt.ylabel("Count")
    plt.xlabel("Degree")
    # plt.xticks(deg)
    plt.xticks(ticks=np.arange(min(deg), max(deg)+1, 1), labels=[str(round(i, 1)) if idx % 10 == 0 else '' for idx, i in enumerate(np.arange(min(deg), max(deg)+1, 1))])
    plt.xticks(rotation=60)  # Rotate x-axis labels for better readability if needed
    plt.show()



if __name__ == '__main__':
    args = init_parser()
    print("---------------------------------------")
    print(f"Dataset: {args.dataset}")
    print("---------------------------------------")
    
    convert_tool(args.dataset)
    G = load_graph("graph.G")
    # graph_show_info(G)
    # graph_degree_to_figure(G)
    # graph_to_figure(G)
