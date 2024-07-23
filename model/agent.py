# user agent model
import json
import time
import random
import logging
from llama_local_api import LlamaApi
from tool.es_manager import ESManager
# from scores_utilities import ScoresUtilities
from model.message import Message
from tool.elastic_search import ElasticSeachStore
import openai
from tool.config_manager import ConfigManager

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
        self.config_manager = ConfigManager('config.ini')
        self.setup_openai()

    def setup_openai(self):
        api_key = self.config_manager.get_api_key()
        openai.api_key = api_key
        
    def set_user_profile(self, uid, profile):
        self.uid = uid
        self.profile = profile

    def set_as_seed(self, initial_message):
        self.is_seed = True
        received_msg = Message(initial_message, self)
        received_msg.set_timestep(timestep=0)
        self.repository.append(received_msg)

        step = 0
        # create user response generation prompt
        prompt = self.message_generate_prompt(step)

        # Llama
        message_content = LlamaApi.llama_generate_messages(prompt)
        print("Seeds message from Llama: ", message_content)

        message = Message(message_content, self)
        message.set_timestep(timestep=step)

        self.posts.append(message)

    def to_dict(self):
        return {
            'id': self.userID,
            'uid': self.uid,
            'status': self.status,
            'posts': [p.content for p in self.posts]
        }

    def update_status(self, status):
        self.status = status

    def calculate_influence_prob(self, influence_prob):
        rand = random.random()
        if rand < influence_prob:
            return True
        else:
            return False

    def message_generate_prompt(self, step):
        user_profile = self.profile
        print("user profile: ", user_profile)
        last_received_msg = self.repository[-1].content
        # print("Last received message: ", last_received_msg)
        # last_post_msg = self.posts[-1].content if self.posts else ""
        topic = self.topic
        # print("topic: ", topic)
        # prompt = user profile + influence message + topic + 
        # Prompt engineering: 1. Prompt with Context (topic), 2. 
        prompt = f"We are building an influence discussion simulation tool, you are a responsible AI, and your task is based on each user's profile, adapt the user's post habit and generate one comment on the topic you received. The format and content should follow the following 3 instructions. Please note, do not generate duplicate sentences from different users. One profile represents one user, and one possible comment only.\
            You are a Large Language Model (LLM) designed to adapt to the user's unique way of speaking. \
            Your task is to simulate comments and responses based on the provided topic, ensuring they align with the user's profile." + \
            f"Based on user profile '{user_profile}', " + \
            f"given the user's last received influence message '{last_received_msg}', " + \
            f"given the topic '{topic}', please perform the following tasks and provide the responses in JSON format, When generating responses, provide some insight around the topic to spark interest in the recipient of your message:" + \
            f"""
                1. Generate one of the user's possible comment while the user reading this topic, in this format: 'Response: [User's response]', each response cannot be the same.
                2. Do a semantic analysis based on the response generated from 1, output the results as this user's opinion in the format of: 'opinion: [Support/Oppose/Neutral]'
                3. Summarize the user's response and generate the response in the format: 'phrases: [List of phrases]'

                Please only return the responses in the following JSON format, one response only for each profile:

                    {{
                        "response": "[User's response]",
                        "opinion": "[Support/Oppose/Neutral]",
                        "phrases": "[List of phrases]"
                    }}
                """
       
        return prompt

    def start_influence(self, step, influence_prob):
        # create user response generation prompt
        prompt = self.message_generate_prompt(step)

        message_content = LlamaApi.llama_generate_messages(prompt)
        print("Response message from Llama: ", message_content)

        # message_content = f"{self.uid} post test at step {step}" # for test only
        
        message = Message(message_content, self)
        message.set_timestep(timestep=step)

        self.posts.append(message)
        # logger.info(str(message))
        
        for v in self.out_neighbors:
            v_agent = self.environment.nodes()[v]["data"]
            is_influenced = v_agent.calculate_influence_prob(influence_prob)

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
                influenced.append(v)
        return influenced
