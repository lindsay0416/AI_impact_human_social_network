import pandas as pd
import os

def combine_csv_files(data_folder, start_step, end_step):
    # Initialize an empty DataFrame to store cumulative data
    cumulative_df = pd.DataFrame()
    
    # Iterate through each step
    for step in range(start_step, end_step + 1):
        current_file = os.path.join(data_folder, f'topic_similarity_results_step{step}.csv')
        
        # Check if the current step CSV file exists
        if os.path.exists(current_file):
            # Load the current step CSV file
            current_df = pd.read_csv(current_file)
            
            # Concatenate the current DataFrame with the cumulative DataFrame
            cumulative_df = pd.concat([cumulative_df, current_df], ignore_index=True)
            
            # Save the updated cumulative DataFrame back to the current step file
            cumulative_df.to_csv(current_file, index=False)
            print(f"Updated data saved to {current_file}")
        else:
            print(f"File not found: {current_file}")

if __name__ == "__main__":
    data_folder = 'Topic_Similarity_Compare_AVG/SYD'  # Adjust this path as necessary
    start_step = 2
    end_step = 15
    combine_csv_files(data_folder, start_step, end_step)
