import os
import json
import matplotlib.pyplot as plt

# Function to read JSON file and generate pie chart
def generate_pie_chart(file_path, city_name="Auckland, NZ"):
    with open(file_path, 'r') as f:
        data = json.load(f)

    # Extracting topic names and text counts from the JSON file, removing double quotes
    topics = []
    for entry in data:
        if "15 words:\n\n" in entry["topic"]:
            topic = entry["topic"].split("15 words:\n\n")[1].replace('"', '')
        elif "15 words:" in entry["topic"]:
            topic = entry["topic"].split("15 words:")[1].replace('"', '').strip()
        elif "Topic:" in entry["topic"]:
            topic = entry["topic"].split("Topic:")[1].replace('"', '').strip()
        else:
            topic = entry["topic"].replace('"', '')
        topics.append(topic)

    text_counts = [entry["text_count"] for entry in data]

    # Calculate percentages
    total_count = sum(text_counts)
    percentages = [(count / total_count) * 100 for count in text_counts]

    # Extract step number from file name, safely check if '_step' is present
    file_name = os.path.basename(file_path)
    if '_step' in file_name:
        step_number = "step" + file_name.split('_step')[1].split('_')[0]  # Keep "step" prefix
    else:
        step_number = "step_unknown"  # Fallback in case '_step' is not found

    title = f"{city_name}: Step {step_number.replace('step', '')}"  # Format title properly
    output_filename = f"topic_{step_number}.pdf"  # Change to .pdf

    # Create the pie chart
    fig, ax = plt.subplots()
    ax.pie(percentages, labels=[f"Topic {i+1}" for i in range(len(topics))], autopct='%1.1f%%', startangle=140)
    ax.legend([f"Topic {i+1}: {topics[i]}" for i in range(len(topics))], loc="center left", bbox_to_anchor=(1, 0.5))

    # Position the title at the bottom left corner
    plt.figtext(0.05, 0.05, title, ha="left", fontsize=12)

    plt.axis('equal')  # Equal aspect ratio ensures that pie chart is drawn as a circle.

    # Create the 'images' folder if it does not exist
    if not os.path.exists('images'):
        os.makedirs('images')

    # Save the chart in the 'images' folder as a PDF
    plt.savefig(os.path.join('images', output_filename), bbox_inches='tight', format='pdf')
    plt.close()  # Close the plot to free memory

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
    plt.xticks(rotation=45)  # Rotate x-axis labels to avoid overlap

    # Create the 'images' folder if it does not exist
    if not os.path.exists('images'):
        os.makedirs('images')

    # Save the plot as a PDF without displaying it
    plt.savefig('images/topic_changes_over_steps.pdf', bbox_inches='tight', format='pdf')
    plt.close()  # Close the plot to free memory

# Folder path containing the JSON files
folder_path = 'extracted_text'  # Update this with the correct path on your local PC

# Loop through the files and generate pie charts
for file_name in os.listdir(folder_path):
    if file_name.endswith('_summary_report.json'):
        file_path = os.path.join(folder_path, file_name)
        generate_pie_chart(file_path)

# Extract the topic counts for each step
step_topic_counts = extract_topic_counts(folder_path)

# Plot the line chart of topic counts
plot_topic_counts(step_topic_counts)
