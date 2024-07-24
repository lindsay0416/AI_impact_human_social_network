import json
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

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

def opinion_counter():
    results = load_result_from_file()
    for simulation in results:
        round = simulation.get("round")
        result = simulation.get("result")
        row = []
        for r in result:
            print(len(r.get("user_data")))

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
    column_means = calculate_coverage()
    # plot_line_chart(column_means)
    opinion_counter()