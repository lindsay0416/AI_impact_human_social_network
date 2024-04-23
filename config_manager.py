import configparser

class ConfigManager:
    def __init__(self, config_file):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

    def get_api_key(self):
        return self.config['openai']['api_key']
