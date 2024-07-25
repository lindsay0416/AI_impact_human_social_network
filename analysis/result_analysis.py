import json
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import re

FONT_SIZE = 14

def load_schema():
    with open("input/parameters.json") as file:
        params = json.load(file)
    return params

def load_result_from_file():
    with open("saved/results.json", "r") as file:
        results = json.load(file)
        results = results.get("simulation")
    return results

def json_formatter(text):
    match = re.search(r'\{(?:[^{}]|)*\}', text)
    if match:
        json_part = match.group()
        return json_part
    else:
        print("No JSON found")
        return None
    
def opinion_counter():
    results = load_result_from_file()
    params = load_schema()

    round = params.get("round")
    timestep = params.get("timestep")

    tables = []
    for simulation in results:
        round = simulation.get("round")
        result = simulation.get("result")
        row = []
        # init a timestep * opinon(3) table for each round
        table = np.zeros((timestep, 3))
        for r in range(0, len(result)):
            counter = {
                "Support": 0,
                "Neutral": 0,
                "Oppose": 0
            }
            user_data = result[r].get("user_data")
            for ud in user_data:
                if len(ud.get("posts")) > 0:
                    post = ud.get("posts")[-1]
                    try:
                        post = json.loads(post)
                    except Exception as e:
                        post = json_formatter(post)
                    if type(post) is str:
                        post = json.loads(post)
                    opinion = post.get("opinion")
                    count = counter.get(opinion)
                    counter[opinion] = count + 1
            print(counter)
            table[r] = list(counter.values())
        tables.append(table)
    results = np.array(tables)
    mean_table = np.mean(results, axis=0)
    print(mean_table)
    return mean_table

def plot_stacked_bar_chart(data):
    timesteps = np.arange(data.shape[0])
    plt.bar(timesteps, data[:, 0], label='Support')
    plt.bar(timesteps, data[:, 1], bottom=data[:, 0], label='Neutral')
    plt.bar(timesteps, data[:, 2], bottom=data[:, 0] + data[:, 1], label='Oppose')

    # Adding labels and title
    plt.xlabel('Timesteps')
    plt.ylabel('Opinion')
    plt.xticks(timesteps)

    # Add a legend
    plt.legend()

    # Show the plot
    plt.show()

def calculate_coverage():
    params = load_schema()
    timestep = params.get("timestep")
    round = params.get("round")
    results = np.zeros((round, timestep))
    results = load_result_from_file()
    rows = []
    for simulation in results:
        round = simulation.get("round")
        result = simulation.get("result")
        row = []
        for r in result:
            coverage = r.get("data").get("coverage")
            row.append(coverage)
        rows.append(row)
    for index, row_values in enumerate(rows):
        results[index] = row_values
    column_means = np.mean(results, axis=0)
    print("Mean of each timestep:", column_means)
    return column_means

def plot_line_chart(series):
    labels = np.arange(len(series))
    # Create a line chart
    fig, ax = plt.subplots()
    ax.plot(labels, series, marker='o', linestyle='-', color='b')  # Line chart

    ax.set_xlabel('Timesteps', fontsize=FONT_SIZE)
    ax.set_ylabel('Influence Coverage', fontsize=FONT_SIZE)

    # Set x-ticks to the generated label values and ensure they are displayed as initial integer labels
    ax.set_xticks(labels)
    ax.set_xticklabels(labels)

    ax.tick_params(axis='both', labelsize=FONT_SIZE)
    plt.show()
    # plt.savefig("saved/coverage.pdf")



def plot_bar_chart(series):
    labels = np.arange(len(series))
    fig, ax = plt.subplots()
    bars = ax.bar(labels, series)

    ax.set_xlabel('Timesteps', fontsize=FONT_SIZE)
    ax.set_ylabel('Influence Coverage', fontsize=FONT_SIZE)

    # Set x-ticks to the generated label values and ensure they are displayed as initial integer labels
    ax.set_xticks(labels)
    ax.set_xticklabels(labels)

    ax.tick_params(axis='both', labelsize=FONT_SIZE)
    plt.show()


if __name__ == "__main__":
    # column_means = calculate_coverage()
    # plot_line_chart(column_means)
    data = opinion_counter()
    plot_stacked_bar_chart(data)