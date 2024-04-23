import openai
from config_manager import ConfigManager
from es_manager import ESManager
from llm_generate_text import GenerateText

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
        

def main():
    app = Application()
    app.check_es_connection()
    app.test_generate_text()

if __name__ == '__main__':
    main()
