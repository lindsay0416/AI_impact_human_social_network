import pandas as pd
import matplotlib.pyplot as plt
import os

def get_max_similarity_scores_and_averages(city_folders, real_world_topics):
    city_average_scores = {}

    for city, folder_path in city_folders.items():
        average_scores_per_step = [0]  # Start with 0 for step 1

        for step in range(2, 16):
            file_path = os.path.join(folder_path, f'topic_similarity_results_step{step}.csv')
            if os.path.exists(file_path):
                df = pd.read_csv(file_path)
                step_scores = []
                for topic in real_world_topics:
                    filtered_df = df[df['real_word_topics'].str.contains(topic, case=False)]
                    max_score = filtered_df['Similarity'].max() if not filtered_df.empty else 0
                    step_scores.append(max_score)
                average_score = sum(step_scores) / len(step_scores) if step_scores else 0
                average_scores_per_step.append(average_score)
            else:
                print(f"File not found: {file_path}")
                average_scores_per_step.append(0)  # Append 0 if file is missing

        city_average_scores[city] = average_scores_per_step

    return city_average_scores

def plot_average_scores(city_scores, steps, cities, output_folder):
    plt.figure(figsize=(10, 6))
    markers = ['o', 's', '^']  # Different markers for each line

    for city_key, city_label in cities.items():
        plt.plot(steps, city_scores[city_key], marker=markers.pop(0), linestyle='-', label=city_label)

    plt.title('Average Maximum Similarity Score by City and Timestep')
    plt.xlabel('Timestep')
    plt.ylabel('Average Maximum Similarity Score')
    plt.xticks(steps)
    plt.grid(True)
    plt.legend()
    
    # Ensure the output directory exists
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, 'avg_top_similarity_scores_comparison.pdf')
    plt.savefig(output_path, format='pdf')
    plt.close()
    print(f"Plot saved to {output_path}")

if __name__ == "__main__":
    city_folders = {
        'Hobart': 'Topic_Similarity_Compare_AVG/Hobart',
        'NZ': 'Topic_Similarity_Compare_AVG/NZ',
        'SYD': 'Topic_Similarity_Compare_AVG/SYD'
    }
    cities = {'Hobart': 'Hobart AU', 'NZ': 'Auckland NZ', 'SYD': 'Sydney AU'}
    output_folder = 'avg_max_topics_similarity_socre'
    steps = list(range(1, 16))  # Now includes Step 1 starting with 0
    real_world_topics = [
        "Alcohol consumption and its effects on health, social habits, and personal choices",
        "Preference for organic wine and concerns about additives in commercial wines.",
        "The Importance of Enjoying Wine Without Judgment or Snobbery",
        "Is over-reliance on organic products causing unnecessary self-imposed suffering?",
        "Health risks of excessive drinking and addiction, with focus on wine consumption"
    ]
    city_scores = get_max_similarity_scores_and_averages(city_folders, real_world_topics)
    plot_average_scores(city_scores, steps, cities, output_folder)
