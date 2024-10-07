import json
import os
import pandas as pd
from sentence_transformers import SentenceTransformer, util

real_world_topics = [
    "Alcohol consumption and its effects on health, social habits, and personal choices",
    "Preference for organic wine and concerns about additives in commercial wines.",
    "The Importance of Enjoying Wine Without Judgment or Snobbery",
    "Is over-reliance on organic products causing unnecessary self-imposed suffering?",
    "Health risks of excessive drinking and addiction, with focus on wine consumption"
]

# Load JSON files and extract topics
def load_topics(json_file_path):
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    topics = []
    for entry in data:
        topic = entry["topic"]
        # Extract topic after "15 words:" or "Topic:"
        if "15 words:" in topic:
            extracted_topic = topic.split("15 words:")[1].strip()
        elif "Topic:" in topic:
            extracted_topic = topic.split("Topic:")[1].strip()
        else:
            extracted_topic = topic.strip()  # Use entire topic if no keyword is found
        topics.append(extracted_topic)
    return topics

# Calculate similarity between two sets of topics
def calculate_similarity(topics1, topics2, model_name='all-MiniLM-L6-v2'):
    model = SentenceTransformer(model_name)
    embeddings1 = model.encode(topics1, convert_to_tensor=True)
    embeddings2 = model.encode(topics2, convert_to_tensor=True)
    
    # Calculate cosine similarity matrix
    similarity_matrix = util.cos_sim(embeddings1, embeddings2)
    
    # Create a DataFrame to store results
    results = []
    for i, topic1 in enumerate(topics1):
        for j, topic2 in enumerate(topics2):
            similarity_score = similarity_matrix[i][j].item()
            results.append({
                'real_word_topics': topic1,
                'simulated_topics': topic2,
                'Similarity': similarity_score
            })
    return pd.DataFrame(results)

# Save the similarity results to a CSV file
def save_to_csv(dataframe, output_file_path):
    dataframe.to_csv(output_file_path, index=False)
    print(f"Similarity results saved to {output_file_path}")

if __name__ == "__main__":
    # Loop through each step file
    for step in range(2, 16):
        simulated_comments_file = f'extracted_text/processed_sentences_step{step}_summary_report.json'
        
        # Check if file exists
        if os.path.exists(simulated_comments_file):
            simulated_topics = load_topics(simulated_comments_file)
            
            # Calculate similarity
            similarity_df = calculate_similarity(real_world_topics, simulated_topics, model_name='all-MiniLM-L6-v2')
            
            # Save results to CSV
            output_csv_path = f'extracted_text/topic_similarity_results_step{step}.csv'
            save_to_csv(similarity_df, output_csv_path)
        else:
            print(f"File not found: {simulated_comments_file}")
