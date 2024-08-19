import pandas as pd
import re
import openai
import json
import configparser
import matplotlib.pyplot as plt  # Importing matplotlib for plotting

# Mock GenerateText class (Replace with your actual implementation if available)
class GenerateText:
     # Function to post data to the /generate_text API and receive the generated text
    @staticmethod
    def get_generated_text(openai, prompt):
        generated_text = ""
        try:
            # Generate text using the OpenAI ChatCompletion endpoint
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a Large Language Model (LLM) designed to adapt to the user's unique way of speaking. \
                     Your task is to simulate comments and responses based on the provided topic, ensuring they align with the user's profile."},
                    {"role": "user", "content": prompt}
                ]
            )
            # Extract the generated text and remove newlines and extra white spaces
            generated_text = response.choices[0].message.content.strip().replace("\n\n", " ").replace("\n", " ")
        except Exception as e:
            print(f"An error occurred: {e}")

        return generated_text, prompt

class ConfigManager:
    def __init__(self, config_file):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

    def get_api_key(self):
        return self.config['openai']['api_key']


class Analysis:
    
    def __init__(self):
        self.config_manager = ConfigManager('config.ini')
        self.setup_openai()

    def setup_openai(self):
        api_key = self.config_manager.get_api_key()
        openai.api_key = api_key

    @staticmethod
    def clean_comment(comment):
        """Cleans the comment text."""
        # Remove non-alphabetic characters and extra spaces
        comment = re.sub(r'[^a-zA-Z\s]', '', comment)
        comment = re.sub(r'\s+', ' ', comment)
        return comment.strip()

    def data_cleaning(self, input_file_path, output_csv_path, output_txt_path):
        # Load the CSV file into a DataFrame
        df = pd.read_csv(input_file_path)

        # Remove records with less than 3 words in the 'commentBody' column
        df['word_count'] = df['commentBody'].apply(lambda x: len(x.split()))
        df = df[df['word_count'] >= 4]

        # Drop duplicate rows
        df = df.drop_duplicates()

        # Clean the text data in 'commentBody'
        df['commentBody'] = df['commentBody'].apply(self.clean_comment)

        # Save the cleaned DataFrame to a new CSV file
        df.to_csv(output_csv_path, index=False)

        # Save comments to a text file, one per line
        with open(output_txt_path, 'w') as file:
            for comment in df['commentBody']:
                file.write(comment + '\n')

        print("Data cleaning completed and files saved.")
        
        return df

    @staticmethod
    def read_comments(file_path):
        with open(file_path, 'r') as file:
            comments = file.readlines()
        return comments

    def analyze_comments_with_llm(self, comments):
        support_count = 0
        oppose_count = 0
        neutral_count = 0

        support_comments = []
        oppose_comments = []
        neutral_comments = []

        for comment in comments:
            prompt = (
                f"You are a responsible AI, you can analyze the sentiment for the input comments. "
                f"Please provide the sentiment of the comment as Support, Oppose, or Neutral. "
                f"Also, return a short explanation for the sentiment.\n\n"
                f"Comment: {comment}\n\n"
                "Response format:\n"
                "{\n"
                '    "sentiment": "Support/Oppose/Neutral",\n'
                '    "explanation": "Short explanation of the sentiment"\n'
                "}\n"
            )

            response, _ = GenerateText.get_generated_text(openai, prompt)

            print(response)

            try:
                result = json.loads(response.strip())
                sentiment = result.get("sentiment")
                explanation = result.get("explanation")

                if sentiment == "Support":
                    support_count += 1
                    support_comments.append(comment)
                elif sentiment == "Oppose":
                    oppose_count += 1
                    oppose_comments.append(comment)
                elif sentiment == "Neutral":
                    neutral_count += 1
                    neutral_comments.append(comment)
            except (json.JSONDecodeError, AttributeError) as e:
                print(f"Error parsing the response: {e}")
                continue

        summary = {
            "Support": {
                "count": support_count,
                "Sample Comments": {i+1: comment for i, comment in enumerate(support_comments[:3])}
            },
            "Oppose": {
                "count": oppose_count,
                "Sample Comments": {i+1: comment for i, comment in enumerate(oppose_comments[:3])}
            },
            "Neutral": {
                "count": neutral_count,
                "Sample Comments": {i+1: comment for i, comment in enumerate(neutral_comments[:3])}
            }
        }

        return summary

    @staticmethod
    def save_summary_to_json(summary, json_file_path):
        # Save the summary to a JSON file
        try:
            with open(json_file_path, 'w') as json_file:
                json.dump(summary, json_file, indent=4)
            print(f"Summary has been successfully saved to {json_file_path}")
        except Exception as e:
            print(f"An error occurred while saving the summary to JSON: {e}")

    @staticmethod
    def plot_summary(summary, plot_file_path):
        # Extract the counts from the summary
        sentiments = ["Support", "Oppose", "Neutral"]
        counts = [summary[sentiment]["count"] for sentiment in sentiments]

        # Create the plot
        plt.figure(figsize=(8, 6))
        plt.bar(sentiments, counts, color=['blue', 'red', 'green'])
        plt.xlabel('Sentiment')
        plt.ylabel('Number of Comments')
        plt.title('Real world comments analysis Summary')

        # Save the plot to a file
        plt.savefig(plot_file_path)

        print(f"Plot saved to {plot_file_path}")

if __name__ == "__main__":
    analysis = Analysis()
    
    # Define the path for the intermediate and output files
    intermediate_csv_path = './dataset/read_wine_dataset_comments.csv'
    output_csv_path = 'cleaned_wine_dataset_comments.csv'
    output_txt_path = 'cleaned_comments.txt'
    summary_json_path = 'comments_summary.json'  # Path to save the summary JSON file
    plot_file_path = 'images/real_world_comments_analysis_summary.png'  # Path to save the plot image

    # Perform data cleaning on the intermediate CSV file
    # analysis.data_cleaning(intermediate_csv_path, output_csv_path, output_txt_path)

    comments = analysis.read_comments(output_txt_path)
    print("Start")
    summary = analysis.analyze_comments_with_llm(comments)

    print(summary)

    # Save the summary to a JSON file
    analysis.save_summary_to_json(summary, summary_json_path)

    # Plot the summary and save to a file
    analysis.plot_summary(summary, plot_file_path)
