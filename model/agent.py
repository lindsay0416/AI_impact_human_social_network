# user agent model
import random
import logging
from model.message import Message

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

    def start_influence(self, step):
        # TODO: use LLM module to create message content
        # TODO: save message to elastic search
        message = Message("this is a test message", self)
        message.set_timestep(timestep=step)
        self.posts.append(message)
        logger.info(str(message))

        for v in self.out_neighbors:
            v_agent = self.environment.nodes()[v]["data"]
            is_influenced = v_agent.calculate_influence_prob()
            if v_agent.status == 0 and is_influenced:
                v_agent.update_status(1)
                v_agent.repository.append(message)


    def calculate_influence_prob(self):
        # TODO: influence prob equation
        influence_prob = INFLUENCE_PROB
        rand = random.random()
        if rand < influence_prob:
            return True
        else:
            return False
