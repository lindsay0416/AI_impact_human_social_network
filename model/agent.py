# user agent model
import random
import logging
# from llama_local_api import LlamaApi
from tool.es_manager import ESManager
# from scores_utilities import ScoresUtilities
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
    def __init__(self, userID, environment, inital_message):
        self.userID = userID
        self.environment = environment
        self.status = 0
        self.repository = []
        self.profile = ""
        self.in_neighbors = []
        self.out_neighbors = []
        self.posts = []
        self.es_manager = ESManager('http://localhost:9200')
        self.is_seed = False
        self.topic = inital_message
    
    def set_user_profile(self, uid, profile):
        self.uid = uid
        self.profile = profile

    def set_as_seed(self, initial_message):
        self.is_seed = True
        message = Message(content=initial_message, sender=self)
        message.set_timestep(0)
        self.posts.append(message)
        self.repository.append(message)

    def to_dict(self):
        return {
            'id': self.userID,
            'uid': self.uid,
            'status': self.status,
            'repository': [str(m) for m in self.repository],
            'posts': [str(p) for p in self.posts]
        }

    def update_status(self, status):
        self.status = status

    def calculate_influence_prob(self):
        influence_prob = INFLUENCE_PROB
        rand = random.random()
        if rand < influence_prob:
            return True
        else:
            return False

    def message_generate_prompt(self, step):
        user_profile = self.profile
        last_received_msg = self.repository[-1].content
        last_post_msg = self.posts[-1].content if self.posts else ""
        topic = self.topic
        prompt =  f"Based on user profile '{user_profile}', " + \
                  f"and its last received influence message '{last_received_msg}', " + \
                  f"and its posting habit '{last_post_msg}', " + \
                  f"what do you think the user would response to '{topic}'?"

        return prompt

    def start_influence(self, step):
        # create user response generation prompt
        prompt = self.message_generate_prompt(step)
        print(prompt)
        
        # create message content through LLM with prompt
        # message_content = LlamaApi.llama_generate_messages(prompt)
        message_content = f"{self.uid} post test at step {step}" # for test only
        
        message = Message(message_content, self)
        message.set_timestep(timestep=step)

        self.posts.append(message)
        # logger.info(str(message))
        
        for v in self.out_neighbors:
            v_agent = self.environment.nodes()[v]["data"]
            is_influenced = v_agent.calculate_influence_prob()

            # Store the sent message to Elasticsearch
            ElasticSeachStore.add_record_to_elasticsearch(
                node=self.uid,
                neigbour=v_agent.uid,
                text=message.content,
                weight=0.1,  # Set an appropriate weight value if needed
                is_received=False,
                es=self.es_manager.es,
                step=step
            )

            if v_agent.status == 0 and is_influenced:
                v_agent.update_status(1)
                v_agent.repository.append(message)
                # Store the received massage
                ElasticSeachStore.add_record_to_elasticsearch(
                    node = v_agent.uid,
                    neigbour= self.uid, 
                    text=message.content,
                    weight=0.1,  # Set an appropriate weight value if needed
                    is_received=True,
                    es=self.es_manager.es,
                    step=step
                )

                # # Save the message to Elasticsearch using ElasticSeachStore
                # # Store the sent message
                # for out_neigbour in self.out_neighbors:
                #     out_neigbour = 'N' + str(out_neigbour)
                #     print(out_neigbour)
                #     ElasticSeachStore.add_record_to_elasticsearch(
                #         node=self.uid,
                #         neigbour=out_neigbour,
                #         text=initial_message,
                #         weight=0.1,  # Set an appropriate weight value if needed
                #         is_received=False,
                #         es=self.es_manager.es,
                #         step=step
                #     )

                # ## Store the received message for each in-neighbor
                # for in_neighbor in self.in_neighbors:
                #     in_neigbour = 'N' + str(in_neighbor)
                #     print(in_neigbour)
                #     ElasticSeachStore.add_record_to_elasticsearch(
                #         node = in_neigbour,
                #         neigbour= self.uid, 
                #         text=initial_message,
                #         weight=0.1,  # Set an appropriate weight value if needed
                #         is_received=True,
                #         es=self.es_manager.es,
                #         step=step
                    # )
# 以下是 Elastic Search 存储的逻辑。
# document_body = {
#             "node": neigbour if is_received else node,
#             "from": node if is_received else None,
#             "to": neigbour if not is_received else None,
#             "received_text": text if is_received else None,
#             "sent_text": text if not is_received else None,
#             "received_text_weight": str(weight) if is_received else None,
#             "timestamp": step,
#         }