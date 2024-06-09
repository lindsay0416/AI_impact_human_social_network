# user agent model
import random

INFLUENCE_PROB = 0.1
#TODO: replce 0.1 with the socre calculated from scores_utilities.py 

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

    def update_status(self, status):
        self.status = status

    def start_influence(self):
        for v in self.out_neighbors:
            v_agent = self.environment.nodes()[v]["data"]
            is_influenced = v_agent.calculate_influence_prob()
            if v_agent.status == 0 and is_influenced:
                v_agent.update_status(1)


    def calculate_influence_prob(self):
        # TODO
        influence_prob = INFLUENCE_PROB
        rand = random.random()
        if rand < influence_prob:
            return True
        else:
            return False
