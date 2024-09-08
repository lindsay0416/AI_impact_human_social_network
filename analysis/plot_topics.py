import os
import json
import matplotlib.pyplot as plt

# Function to read JSON file and extract the number of topics for each step
def extract_topic_counts(folder_path):
    step_topic_counts = {}
    
    for file_name in os.listdir(folder_path):
        if file_name.endswith('_summary_report.json'):
            file_path = os.path.join(folder_path, file_name)
            
            # Extract step number
            step_number = "Step " + file_name.split('_step')[1].split('_')[0] if '_step' in file_name else "Unknown Step"
            
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Count number of topics
            topic_count = len(data)
            step_topic_counts[step_number] = topic_count
    
    return step_topic_counts

# Function to plot line chart of topic counts
def plot_topic_counts(step_topic_counts, city_name="Auckland, NZ"):
    # Sort steps by their number
    steps = sorted(step_topic_counts.keys(), key=lambda x: int(x.split(" ")[1]) if x.split(" ")[1].isdigit() else float('inf'))
    topic_counts = [step_topic_counts[step] for step in steps]
    
    plt.figure()
    plt.plot(steps, topic_counts, marker='o', linestyle='-', color='b')
    plt.title(city_name)
    plt.xlabel('Step')
    plt.ylabel('Number of Topics')
    
    # Save the plot as a PDF
    if not os.path.exists('images'):
        os.makedirs('images')
    plt.savefig('images/topic_changes_over_steps.pdf', bbox_inches='tight', format='pdf')
    plt.show()

# Folder path containing the JSON files
folder_path = 'extracted_text'  # Update this with the correct path on your local PC

# Extract the topic counts for each step
step_topic_counts = extract_topic_counts(folder_path)

# Plot the line chart of topic counts
plot_topic_counts(step_topic_counts)
