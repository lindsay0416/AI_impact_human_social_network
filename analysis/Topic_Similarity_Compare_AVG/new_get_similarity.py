import os
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import pandas as pd

# Load BERT model for embedding
model = SentenceTransformer('bert-base-nli-mean-tokens')

# Function to calculate cosine similarity between real and simulated topics
def calculate_similarity(df):
    # Encode the sentences using BERT embeddings
    real_word_embeddings = model.encode(df['real_word_topics'].tolist())
    simulated_word_embeddings = model.encode(df['simulated_topics'].tolist())

    # Calculate cosine similarity for each row
    similarities = []
    for real, sim in zip(real_word_embeddings, simulated_word_embeddings):
        similarities.append(cosine_similarity([real], [sim])[0][0])

    # Add new column with similarity scores
    df['new_similarity'] = similarities
    return df

# Define folder path
folder_path = 'SYD'

# Automatically generate file paths from step 2 to step 15 inside 'Hobart' folder
file_paths = [os.path.join(folder_path, f'topic_similarity_results_step{i}.csv') for i in range(2, 16)]

# Process each file and save the result
for file_path in file_paths:
    if os.path.exists(file_path):  # Check if the file exists
        df = pd.read_csv(file_path)
        df_with_similarity = calculate_similarity(df)
        output_file_path = file_path.replace('.csv', '_with_similarity.csv')
        df_with_similarity.to_csv(output_file_path, index=False)

print("Processing complete.")
