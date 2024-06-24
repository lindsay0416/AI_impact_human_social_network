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

    def calculate_influence_prob(self):
        # TODO: influence prob equation
        influence_prob = INFLUENCE_PROB
        rand = random.random()
        if rand < influence_prob:
            return True
        else:
            return False

    def start_influence(self, step):
        initial_message = "This is a test post message"
        message = Message(initial_message, self)
        message.set_timestep(timestep=step)
        self.posts.append(message)
        logger.info(str(message))

        for v in self.out_neighbors:
            print("vvvvvvvv", v)
            v_agent = self.environment.nodes()[v]["data"]
            print("v_agent: ", self.userID)
            is_influenced = v_agent.calculate_influence_prob()
            print("is_influenced: ", is_influenced)
            if v_agent.status == 0 and is_influenced:
                v_agent.update_status(1)
                v_agent.repository.append(message)
                
                # Generate message content using the LLM module
                initial_message = LlamaApi.llama_generate_messages(initial_message)
                print("generated_messages:", initial_message)
 
                # Save the message to Elasticsearch using ElasticSeachStore
                # Store the sent message
                for in_neighbor in self.in_neighbors:
                    in_neigbour = 'N' + str(in_neighbor)
                    print(in_neigbour)
                    ElasticSeachStore.add_record_to_elasticsearch(
                        node=self.uid,
                        in_neigbour=in_neigbour,
                        text=initial_message,
                        weight=0.1,  # Set an appropriate weight value if needed
                        is_received=False,
                        es=self.es_manager.es,
                        step=step
                    )

                ## Store the received message for each in-neighbor
                for in_neighbor in self.in_neighbors:
                    in_neigbour = 'N' + str(in_neighbor)
                    print(in_neigbour)
                    ElasticSeachStore.add_record_to_elasticsearch(
                        node=self.uid,
                        in_neigbour=in_neigbour,
                        text=initial_message,
                        weight=0.1,  # Set an appropriate weight value if needed
                        is_received=True,
                        es=self.es_manager.es,
                        step=step
                    )
# 以下是 Elastic Search 存储的逻辑。
# document_body = {
#             "node": in_neigbour if is_received else node,
#             "from": node if is_received else None,
#             "to": in_neigbour if not is_received else None,
#             "received_text": text if is_received else None,
#             "sent_text": text if not is_received else None,
#             "received_text_weight": str(weight) if is_received else None,
#             "timestamp": step,
#         }