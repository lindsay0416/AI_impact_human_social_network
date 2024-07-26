import json
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import re
from wordcloud import WordCloud

FONT_SIZE = 14

def load_schema():
    with open("input/parameters.json") as file:
        params = json.load(file)
    return params

def load_user_profile():
    with open("input/user_profile.json") as file:
        profiles = json.load(file)
    return profiles

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

def profile_statistics(opinion):
    results = load_result_from_file()
    params = load_schema()
    profiles = load_user_profile()

    timestep = params.get("timestep")
    round = params.get("round")

    rounds = []
    for simulation in results:
        result = simulation.get("result")
        user_data = result[-1].get("user_data")
        users = []
        for ud in user_data:
            if len(ud.get("posts")) > 0:
                post = ud.get("posts")[-1]
                try:
                    post = json.loads(post)
                except Exception as e:
                    post = json_formatter(post)
                if type(post) is str:
                    post = json.loads(post)
                if post.get("opinion") == opinion:
                    users.append(ud.get("uid"))
        rounds.append(users)
    
    gender_distribution = np.zeros((round, 2))
    for r in range(0, len(rounds)):
        age_counter = {}
        # gender_counter = {
        #                     "male": 0,
        #                     "female": 0
        #                 }
        for uid in rounds[r]:
            age = profiles.get(uid).get("age")
            if age_counter.get(age) is None:
                age_counter[age] = 1
            else:
                age_counter[age] = age_counter.get(age) + 1
        print(age_counter)
        #     gender = profiles.get(uid).get("gender")
        #     # print(gender)
        #     gender_counter[gender] = gender_counter.get(gender) + 1
        # print(gender_counter)
    



def phrases_counter():
    results = load_result_from_file()
    params = load_schema()
    timestep = params.get("timestep")

    dicts = []
    for simulation in results:
        result = simulation.get("result")
        # init a timestep * opinon(3) table for each round
        table = np.zeros((timestep, 3))
        # for r in range(0, len(result)):
        counter = {}
        user_data = result[-1].get("user_data")
        for ud in user_data:
            if len(ud.get("posts")) > 0:
                post = ud.get("posts")[-1]
                try:
                    post = json.loads(post)
                except Exception as e:
                    post = json_formatter(post)
                if type(post) is str:
                    post = json.loads(post)
                phrases = post.get("phrases").split(",")
                for p in phrases:
                    p = p.strip()
                    if counter.get(p) is None:
                        counter[p] = 1
                    else:
                        counter[p] = counter.get(p) + 1
        counter = dict(sorted(counter.items(), key=lambda item: item[1], reverse=True))
        dicts.append(counter)
    cumulative_counts = {}
    appearance_counts = {}

    # Iterate through each dictionary
    for d in dicts:
        for key, value in d.items():
            if key in cumulative_counts:
                cumulative_counts[key] += value
                appearance_counts[key] += 1
            else:
                cumulative_counts[key] = value
                appearance_counts[key] = 1

    average_appearance = {key: cumulative_counts[key] / appearance_counts[key] for key in cumulative_counts}
    average_appearance = dict(sorted(average_appearance.items(), key=lambda item: item[1], reverse=True))
    print(average_appearance)
    return average_appearance

def plot_word_cloud(phrases_dict):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(phrases_dict)

    # Display the generated word cloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    # plt.show()
    plt.savefig("saved/phrases.pdf")

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
    plt.xlabel('Timesteps', fontsize=FONT_SIZE)
    plt.ylabel('Opinion', fontsize=FONT_SIZE)
    plt.xticks(timesteps)
    
    # plt.set_yticks(np.arange(0, 21, 1))

    # Add a legend
    plt.legend(fontsize=FONT_SIZE)

    # Show the plot
    # plt.show()
    
    plt.savefig("saved/opinion.pdf")

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
    ax.set_yticks(np.arange(0, 16, 2))

    ax.tick_params(axis='both', labelsize=FONT_SIZE)
    # plt.show()
    plt.savefig("saved/coverage.pdf")



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
    # data = opinion_counter()
    # plot_stacked_bar_chart(data)
    # phrases = phrases_counter()
    # plot_word_cloud(phrases)
    profile_statistics("Support")