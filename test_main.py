import openai
from config_manager import ConfigManager
from es_manager import ESManager
from llm_generate_text import GenerateText
from elastic_search import ElasticSeachStore
from sentence_embedding import Text2Vector
from llama_local_api import LlamaApi

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
        node = "N39"
        connected_node = "N1"
        text = "Test add record to elasticsearch."
        weight = 1
        is_received = False
        es_client = self.es_manager.es  # Access the Elasticsearch client directly
        response = ElasticSeachStore.add_record_to_elasticsearch(node, connected_node, text, weight, is_received, es_client)
        print("response from elastic search:", response)

    def test_embedding_text(self):
        diffusion_message = "Sky is blue."
        embedding = Text2Vector.get_embedding(diffusion_message)
        print(embedding)
    
    def test_received_text_cosine_similarity(self):
        diffusion_message = "Sky is blue."
        index_name = "received_text_test01"
        es_client = self.es_manager.es
        results = Text2Vector.received_text_cosine_similarity(index_name, diffusion_message, es_client)
        print(results)
        texts = Text2Vector.get_messages_from_list(results) # print the list of texts
        print(texts)

    def test_sent_text_cosine_similarity(self):
        diffusion_message = "Sky is blue."
        index_name = "sent_text_test01"
        es_client = self.es_manager.es
        results = Text2Vector.sent_text_cosine_similarity(index_name, diffusion_message, es_client)
        print(results)
        texts = Text2Vector.get_messages_from_list(results) # print the list of texts
        print(texts)
    def test_get_generated_text(self):
        prompt = "How are you!"
        result = LlamaApi.generate_messages_with_timestamps(prompt)
        print(result[0]['timestamp'])
        print(result[0]['message'])



def main():
    app = Application()
    app.check_es_connection()
    # app.test_generate_text()

    # app.test_add_record_to_elasticsearch()
    
    # app.test_embedding_text()

    # app.test_received_text_cosine_similarity()
    # app.test_sent_text_cosine_similarity()
    app.test_get_generated_text()

if __name__ == '__main__':
    main()
