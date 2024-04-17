from elasticsearch import Elasticsearch
from llm_generate_text import GenerateText
import openai
import configparser


def main():
    # Connect to local Elasticsearch instance
    es = Elasticsearch("http://localhost:9200")

    # Check if Elasticsearch is running
    if es.ping():
        print("Connected to Elasticsearch")
    else:
        print("Could not connect to Elasticsearch")

    
    # Read API key from config
    config = configparser.ConfigParser()
    config.read('config.ini')
    api_key = config['openai']['api_key']
    # Set the OpenAI API key
    openai.api_key = api_key


if __name__ == '__main__':
    main()