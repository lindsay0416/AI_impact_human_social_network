import string
from nltk.tokenize import sent_tokenize
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sentence_transformers import SentenceTransformer
import matplotlib.pyplot as plt
import nltk
import json
from llama_local_api import LlamaApi
import os

# Ensure NLTK punkt tokenizer is downloaded
nltk.download('punkt')

class TextTopicAnalyzer:
    def __init__(self, input_file_path, output_file_path, model_name='all-MiniLM-L6-v2'):
        self.input_file_path = input_file_path
        self.output_file_path = output_file_path
        self.model = SentenceTransformer(model_name)
        self.sentences = []
        self.clustered_sentences = []  # List to store each cluster in a separate array
        self.summaries = []

    def preprocess_text(self, text):
        """Preprocess a single sentence by lowercasing, removing punctuation, and trimming whitespace."""
        text = text.lower()
        text = text.translate(str.maketrans('', '', string.punctuation))
        text = text.strip()
        return text

    def load_and_preprocess_sentences(self):
        """Load the text, split into sentences, and preprocess each sentence."""
        with open(self.input_file_path, 'r') as infile:
            text = infile.read()
            sentences = sent_tokenize(text)
            self.sentences = [self.preprocess_text(sentence) for sentence in sentences]

    def save_preprocessed_sentences(self):
        """Save the preprocessed sentences to the output file."""
        with open(self.output_file_path, 'w') as outfile:
            for sentence in self.sentences:
                outfile.write(sentence + '\n')

    def find_optimal_k(self, min_k, max_k):
        """Find the optimal number of clusters using Silhouette Score."""
        if not self.sentences:
            print("No sentences to process. Make sure to load and preprocess sentences first.")
            return None

        embeddings = self.model.encode(self.sentences)

        best_k = None
        best_silhouette = -1
        k_range = range(min_k, min(max_k, len(self.sentences)) + 1)
        silhouette_scores = []

        for k in k_range:
            kmeans = KMeans(n_clusters=k, random_state=42)
            kmeans.fit(embeddings)
            score = silhouette_score(embeddings, kmeans.labels_)
            silhouette_scores.append(score)
            if score > best_silhouette:
                best_silhouette = score
                best_k = k

        # Plot the Silhouette Scores
        plt.figure()
        plt.plot(k_range, silhouette_scores, 'b-')
        plt.xlabel('Number of clusters (k)')
        plt.ylabel('Silhouette Score')
        plt.title('Silhouette Score for different k values')

        # Save the figure
        images_dir = "images"
        os.makedirs(images_dir, exist_ok=True)
        plot_path = os.path.join(images_dir, 'silhouette_score_plot.png')
        plt.savefig(plot_path)
        plt.show()

        print(f"Silhouette score plot saved to {plot_path}")

        return best_k

    def cluster_sentences(self, k):
        """Cluster the sentences using K-means with the specified number of clusters."""
        if not self.sentences:
            print("No sentences to process. Make sure to load and preprocess sentences first.")
            return

        embeddings = self.model.encode(self.sentences)
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(embeddings)
        labels = kmeans.labels_

        self.clustered_sentences = [[] for _ in range(k)]  # Create a list of lists for each cluster
        for label, sentence in zip(labels, self.sentences):
            self.clustered_sentences[label].append(sentence)

    def summarize_clusters(self):
        """Summarize each cluster using an LLM."""
        if not self.clustered_sentences:
            print("No clusters to summarize. Make sure to cluster the sentences first.")
            return

        self.summaries = []
        for i, cluster in enumerate(self.clustered_sentences):
            generate_prompt = f"Generate one topic of the following text within 20 words:\n\n" + "\n".join(cluster)
            response = LlamaApi.llama_generate_messages(generate_prompt)
            self.summaries.append(response)

    def generate_json_report(self):
        """Generate a JSON report containing the cluster summaries and save to a file."""
        if not self.summaries:
            print("No summaries found. Make sure to summarize the clusters first.")
            return

        report = []
        for i, summary in enumerate(self.summaries):
            cluster_info = {
                "cluster": i + 1,
                "topic": summary,
                "text_count": len(self.clustered_sentences[i]),  # Add the count of texts in the cluster
                "sentences": self.clustered_sentences[i]
            }
            report.append(cluster_info)

        # Save the report to a JSON file
        json_output_path = self.output_file_path.replace('.txt', '_summary_report.json')
        with open(json_output_path, 'w') as json_file:
            json.dump(report, json_file, indent=4)

        print(f"JSON report saved to {json_output_path}")

# Example usage:
# Initialize the TextTopicAnalyzer class
analyzer = TextTopicAnalyzer(input_file_path='extracted_text/simulation_response_only.txt',
                             output_file_path='extracted_text/processed_sentences.txt')

# Load and preprocess sentences
analyzer.load_and_preprocess_sentences()

# Save the preprocessed sentences to a file
analyzer.save_preprocessed_sentences()

# Find the optimal number of clusters
optimal_k = analyzer.find_optimal_k(8, 30)

# Cluster the sentences using the optimal number of clusters
analyzer.cluster_sentences(optimal_k)

# Summarize each cluster using LLM
analyzer.summarize_clusters()

# Generate and save the JSON report
analyzer.generate_json_report()
