# user agent model
import random
import logging
from llama_local_api import LlamaApi
from tool.es_manager import ESManager
from scores_utilities import ScoresUtilities
from model.message import Message
from tool.elastic_search import ElasticSeachStore

INFLUENCE_PROB = 0.1
#TODO: replce 0.1 with the socre calculated from scores_utilities.py 

# init logger
logger = logging.getLogger("agent")
logging.basicConfig(level="INFO")

class Agent:
    """
        Init a user agent object. A user agent holds the following attributes:
            - status: active or inactive; represented by 1 (for active) and 0 (for inactive)

    """
    def __init__(self, userID, environment):
        self.userID = userID
        self.environment = environment
        self.status = 0
        self.repository = []
        self.profile = ""
        self.in_neighbors = []
        self.out_neighbors = []
        self.posts = []
        self.es_manager = ESManager('http://localhost:9200')
    
    def set_user_profile(self, uid, profile):
        self.uid = uid
        self.profile = profile
    
    def to_dict(self):
        return{
            'id': self.userID,
            'uid': self.uid,
            'status': self.status,
            'profile': self.profile,
            'repository': [str(m) for m in self.repository],
            'posts': [str(p) for p in self.posts],
            'in_neighbors': self.in_neighbors,
            'out_neighbors': self.out_neighbors
        }

    def update_status(self, status):
        self.status = status

    # def start_influence(self, step):
    #     es_client = self.es_manager.es
    #     # TODO: use LLM module to create message content
    #     # TODO: save message to elastic search
    #     initial_message = "this is a test message"
    #     message = Message(initial_message, self)
    #     message.set_timestep(timestep=step)
    #     self.posts.append(message)
    #     logger.info(str(message))

    #     for v in self.out_neighbors:
    #         v_agent = self.environment.nodes()[v]["data"]
    #         is_influenced = v_agent.calculate_influence_prob()
    #         if v_agent.status == 0 and is_influenced:
    #             v_agent.update_status(1)
    #             v_agent.repository.append(message)

    def calculate_influence_prob(self):
        # TODO: influence prob equation
        influence_prob = INFLUENCE_PROB
        rand = random.random()
        if rand < influence_prob:
            return True
        else:
            return False

    def start_influence(self, step):
        # es_client = self.es_manager.es
        initial_message = "this is a test message"
        message = Message(initial_message, self)
        message.set_timestep(timestep=step)
        self.posts.append(message)
        logger.info(str(message))

        for v in self.out_neighbors:
            v_agent = self.environment.nodes()[v]["data"]
            is_influenced = v_agent.calculate_influence_prob()
            if v_agent.status == 0 and is_influenced:
                v_agent.update_status(1)
                v_agent.repository.append(message)
                
                # Generate message content using the LLM module
                generated_messages = LlamaApi.generate_messages_with_timestamps(initial_message)
                next_message = generated_messages[0]['message']
                # No need to get timestamp from generated messages now

                # Save the message to Elasticsearch
                # Store the sent message
                self.es_manager.index(
                    index_name='sent_text_test01',
                    document_body={
                        'from': self,
                        'node': v,
                        'sent_text': initial_message,
                        'sent_text_vector': ScoresUtilities.get_embedding(initial_message),
                        'timestep': step  # Store timestep instead of timestamp
                    }
                )

                # Store the received message
                self.es_manager.index(
                    index_name='received_text_test01',
                    document_body={
                        'from': self,
                        'node': v,
                        'received_text': initial_message,
                        'received_text_vector': ScoresUtilities.get_embedding(initial_message),
                        'timestep': step  # Store timestep instead of timestamp
                    }
                )

                # Update for the next iteration
                initial_message = next_message
class Message:
    def __init__(self, content, agent):
        self.content = content
        self.agent = agent
        self.timestamp = None

    def set_timestep(self, timestep):
        self.timestamp = timestep

    def __str__(self):
        return f"Message(content={self.content}, timestamp={self.timestamp})"
    

# Example usage:
# Assuming Text2Vector class and LlamaApi class are defined elsewhere
# and have the methods used above.
if __name__ == "__main__":
    from elasticsearch import Elasticsearch
    es_manager = ESManager(host_url='http://localhost:9200')  # Update with your Elasticsearch host URL
    environment = {}  # Initialize this with the actual environment data
    agent = Agent(es_manager, environment)
    agent.start_influence(step=1)