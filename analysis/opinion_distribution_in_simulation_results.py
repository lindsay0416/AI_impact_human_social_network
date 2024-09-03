import re
import os
import matplotlib.pyplot as plt

def load_opinions(file_path):
    """Load opinions from the file and count them."""
    with open(file_path, 'r') as file:
        content = file.read()

    # Use regex to find all "opinion": "..." occurrences
    opinions = re.findall(r'"opinion":\s*"([^"]+)"', content)

    # Count the occurrences of each opinion
    opinion_counts = {}
    for opinion in opinions:
        if opinion in opinion_counts:
            opinion_counts[opinion] += 1
        else:
            opinion_counts[opinion] = 1

    return opinion_counts

def plot_opinion_distribution(opinion_counts):
    """Plot a graph of the opinion distribution."""
    total_opinions = sum(opinion_counts.values())

    # Calculate percentages for each opinion
    opinions = list(opinion_counts.keys())
    percentages = [(count / total_opinions) * 100 for count in opinion_counts.values()]

    # Plotting
    plt.figure(figsize=(8, 6))
    plt.bar(opinions, percentages, color='skyblue')
    plt.xlabel('Opinion')
    plt.ylabel('Percentage (%)')
    plt.title('Opinion Distribution')
    plt.ylim(0, 100)  # Set y-axis limit to 100% for better visualization
    plt.grid(axis='y')

    # Save the plot to the 'images' folder
    images_dir = 'images'
    os.makedirs(images_dir, exist_ok=True)
    plot_path = os.path.join(images_dir, 'opinion_distribution.png')
    plt.savefig(plot_path)
    plt.show()

    print(f"Plot saved to {plot_path}")

if __name__ == "__main__":
    # Path to the input file
    file_path = 'extracted_text/simulation_response_with_opinion.txt'

    # Load opinions and count them
    opinion_counts = load_opinions(file_path)

    # Plot the opinion distribution
    plot_opinion_distribution(opinion_counts)
