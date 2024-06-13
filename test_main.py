import openai
from tool.config_manager import ConfigManager
from tool.es_manager import ESManager
from llm_generate_text import GenerateText
from tool.elastic_search import ElasticSeachStore
from sentence_embedding import Text2Vector
from llama_local_api import LlamaApi
from scores_utilities import ScoresUtilities
import json
import numpy as np

class Application:
    def __init__(self):
        self.config_manager = ConfigManager('config.ini')
        self.es_manager = ESManager('http://localhost:9200')
        self.setup_openai()

    def setup_openai(self):
        api_key = self.config_manager.get_api_key()
        openai.api_key = api_key

    def check_es_connection(self):
        if self.es_manager.is_connected():
            print("Connected to Elasticsearch")
        else:
            print("Could not connect to Elasticsearch")

    def test_generate_text(self):
        prompt = "Hello"
        generated_text, prompt = GenerateText.get_generated_text(openai, prompt)
        print("Prompt:", prompt)
        print("Generated Text:", generated_text)

    def test_add_record_to_elasticsearch(self):
        node = "N1"
        connected_node = "N9"
        text = "Test add record to elasticsearch."
        weight = 0.8
        is_received = False
        es_client = self.es_manager.es  # Access the Elasticsearch client directly
        response = ElasticSeachStore.add_record_to_elasticsearch(node, connected_node, text, weight, is_received, es_client)
        print("response from elastic search:", response)

    def test_embedding_text(self):
        diffusion_message = "Test record in elasticsearch."
        embedding = Text2Vector.get_embedding(diffusion_message)
        print(embedding)
    
    def test_received_text_cosine_similarity(self):
        diffusion_message = "Test record in elasticsearch."
        index_name = "received_text_test01"
        es_client = self.es_manager.es
        node = "N1"
        results = Text2Vector.received_text_cosine_similarity(index_name, diffusion_message, node, es_client)
        print(results)
        texts = Text2Vector.get_messages_from_list(results) # print the list of texts
        print("received_text_cosine_similarity: ", texts)

    def test_sent_text_cosine_similarity(self):
        diffusion_message = "Test record in elasticsearch."
        index_name = "sent_text_test01"
        es_client = self.es_manager.es
        node = "N1"
        results = Text2Vector.sent_text_cosine_similarity(index_name, diffusion_message,node, es_client)
        print(results)
        texts = Text2Vector.get_messages_from_list(results) # print the list of texts
        print("sent_text_cosine_similarity: ", texts)

    def generate_response_messages_with_timestamps(self):
        # Example JSON data
        user_data = {
            "N1": {
                "name": "Emily",
                "age": 32,
                "gender": "female",
                "description": "a passionate artist who loves expressing herself through paintings. She finds inspiration in nature and often exhibits her artwork in local galleries."
            },
            "N2": {
                "name": "James",
                "age": 25,
                "gender": "male",
                "description": "a tech-savvy enthusiast who spends most of his time exploring the latest gadgets and software. He enjoys coding and is always up-to-date with the latest technological advancements."
            },
            "N3": {
                "name": "Olivia",
                "age": 42,
                "gender": "female",
                "description": "a dedicated yoga instructor who believes in the power of mindfulness and physical well-being. She enjoys teaching others and creating a peaceful environment for her students."
            }
        }

        # Convert the dictionary to a JSON string
        json_data = json.dumps(user_data, indent=2)

        # Prepare the prompt
        prompt = f"Here is some user data in JSON format:\n\n{json_data}\n\nPlease summarize the information provided."
        # prompt = "How are you!"
        result = LlamaApi.generate_messages_with_timestamps(prompt)
        print(result[0]['timestamp'])
        print(result[0]['message'])

    def test_calculate_time_decay_and_similarity(self):
        diffusion_message = "Test record in elasticsearch."
        prompt = "How are you!"
        node = "N1"
        es_client = self.es_manager.es

        time_decay_data = ScoresUtilities.calculate_time_decay_and_similarity(es_client, diffusion_message, prompt, node)
        print(time_decay_data)

        # Read and print correlation data
        correlation_data = ScoresUtilities.read_correlation_data(time_decay_data)
        print(correlation_data)

        # Read and print messages
        print("Received Messages:", time_decay_data['received_messages'])
        print("Sent Messages:", time_decay_data['sent_messages'])

    def test_read_correlation_data(self):
        diffusion_message = "Test record in elasticsearch."
        prompt = "How are you!"
        node = "N1"
        es_client = self.es_manager.es

        # Calculate the time decay and similarity data
        time_decay_data = ScoresUtilities.calculate_time_decay_and_similarity(es_client, diffusion_message, prompt, node)

        # Read the correlation data
        correlation_data = ScoresUtilities.read_correlation_data(time_decay_data)

        # Print the correlation data
        print("Probabilities: ", correlation_data['probabilities'])
        print("Retrieved Sent Message Similarity: ", correlation_data['retrieved_sent_message_similarity'])
        print("Retrieved Received Message Similarity: ", correlation_data['retrieved_received_message_similarity'])

        # Read and print messages
        print("Received Messages:", time_decay_data['received_messages'])
        print("Sent Messages:", time_decay_data['sent_messages'])

    def test_profile_similarity(self):
        Node = "N1"
        response = ScoresUtilities.profile_similarity(Node)
        print(response)

def main():
    app = Application()
    app.check_es_connection()
    # app.test_generate_text()

    # app.test_add_record_to_elasticsearch()
    
    # app.test_embedding_text()

    # app.test_received_text_cosine_similarity()
    # app.test_sent_text_cosine_similarity()
    # app.generate_response_messages_with_timestamps()
    # app.test_calculate_time_decay_and_similarity()
    # app.test_read_correlation_data()
    app.test_profile_similarity()

if __name__ == '__main__':
    main()
