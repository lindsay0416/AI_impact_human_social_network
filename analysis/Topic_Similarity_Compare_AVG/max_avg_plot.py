import os
import pandas as pd
import matplotlib.pyplot as plt

# Define the folders and their corresponding names for the plot
folders = {
    'Hobart': 'Hobart AU',
    'NZ': 'Auckland NZ',
    'SYD': 'Sydney AU'
}

# Initialize a dictionary to store the average maximum similarities for each location
location_similarities = {location_name: [] for location_name in folders.values()}

# Steps from 2 to 15
steps = range(2, 16)

# Base folder where the CSV files are located (parent directory of the script)
base_folder = os.path.dirname(os.path.abspath(__file__))

# Process each folder
for folder, location_name in folders.items():
    # List to hold average maximum similarities for this location
    avg_max_similarities = []
    
    # Process files from step 2 to step 15
    for step in steps:
        # Construct the file path using the folder and step number
        file_name = f'topic_similarity_results_step{step}_with_similarity.csv'
        file_path = os.path.join(base_folder, folder, file_name)
        
        try:
            # Read the CSV file
            df = pd.read_csv(file_path)
            
            # Ensure the necessary columns exist
            if 'real_word_topics' in df.columns and 'new_similarity' in df.columns:
                # Find the 5 unique topics in 'real_word_topics'
                unique_topics = df['real_word_topics'].unique()
                
                max_similarities = []
                # For each topic, find the maximum 'new_similarity' score
                for topic in unique_topics:
                    topic_df = df[df['real_word_topics'] == topic]
                    max_similarity = topic_df['new_similarity'].max()
                    max_similarities.append(max_similarity)
                
                # Calculate the average of the maximum similarities
                avg_max_similarity = sum(max_similarities) / len(max_similarities)
                avg_max_similarities.append(avg_max_similarity)
            else:
                print(f"Columns 'real_word_topics' or 'new_similarity' not found in {file_path}")
                avg_max_similarities.append(None)
        except FileNotFoundError:
            print(f"File {file_path} does not exist.")
            avg_max_similarities.append(None)
    
    # Store the average maximum similarities for this location
    location_similarities[location_name] = avg_max_similarities

# Plotting the results
plt.figure(figsize=(12, 6))

for location_name, similarities in location_similarities.items():
    # Only include steps where data is available
    available_steps = [step for step, sim in zip(steps, similarities) if sim is not None]
    available_similarities = [sim for sim in similarities if sim is not None]
    
    plt.plot(available_steps, available_similarities, marker='o', label=location_name)

plt.title('Average Maximum Similarity Scores from Step 2 to Step 15')
plt.xlabel('Step')
plt.ylabel('Average Maximum Similarity Score')
plt.legend()
plt.grid(True)
plt.xticks(steps)  # Ensure all steps are shown on the x-axis
plt.tight_layout()

# Save the plot in the 'Topic_Similarity_Compare_AVG' folder
output_path = os.path.join(base_folder, 'average_max_similarity_scores.pdf')
plt.savefig(output_path, format='pdf')
plt.show()
