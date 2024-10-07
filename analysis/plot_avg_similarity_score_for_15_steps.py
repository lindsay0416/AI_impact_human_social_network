import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_avg_similarity(data_folders, output_plot_file, csv_output_folder):
    # Ensure the output folder for CSV files exists
    os.makedirs(csv_output_folder, exist_ok=True)

    # Define the range of steps, including step 1 to step 15
    steps = range(1, 16)
    cities = {'Hobart': 'Hobart', 'NZ': 'Auckland_NZ', 'SYD': 'Sydney_AU'}
    colors = ['b', 'g', 'r']  # Different colors for each city line
    markers = ['o', 's', '^']  # Different markers for each city line
    plt.figure(figsize=(10, 5))
    
    # Process each city
    for city_folder, city_name in cities.items():
        data_folder = os.path.join(data_folders, city_folder)
        avg_similarities = [0]  # Start with 0 for step 1
        output_csv_file = os.path.join(csv_output_folder, f'{city_name}_avg_similarity_score.csv')  # CSV path

        # Loop through each step file from step 2 to step 15
        for step in range(2, 16):
            csv_file = f'{data_folder}/topic_similarity_results_step{step}.csv'
            
            # Check if the file exists
            if os.path.exists(csv_file):
                # Read the CSV file
                df = pd.read_csv(csv_file)
                
                # Calculate the average similarity
                avg_similarity = df['Similarity'].mean()
                avg_similarities.append(avg_similarity)
            else:
                print(f"File not found: {csv_file}")
                avg_similarities.append(None)

        # Create DataFrame from results
        results_df = pd.DataFrame({
            'Timestep': list(steps),
            'Average Similarity': avg_similarities
        })

        # Save results to a CSV file for the city
        results_df.to_csv(output_csv_file, index=False)
        print(f"Average similarity results saved to {output_csv_file}")

        # Plotting the average similarities for the current city
        plt.plot(steps, avg_similarities, marker=markers.pop(0), linestyle='-', color=colors.pop(0), label=city_name)

    # Final plot adjustments
    plt.title('Average Similarity Score by Timestep for Each City')
    plt.xlabel('Timestep')
    plt.ylabel('Average Similarity Score')
    plt.grid(True)
    plt.xticks(steps)
    plt.ylim(0, 1)  # Assuming similarity scores range from 0 to 1
    plt.legend()

    # Save the plot to a file as PDF
    plt.savefig(output_plot_file, format='pdf')
    plt.show()

if __name__ == "__main__":
    data_folders = 'Topic_Similarity_Compare_AVG'
    output_plot_file = 'avg_max_topics_similarity_socre/avg_similarity_scores_comparison.pdf'
    csv_output_folder = 'avg_max_topics_similarity_socre'
    plot_avg_similarity(data_folders, output_plot_file, csv_output_folder)
