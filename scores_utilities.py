# This function is about the message retrieve:
# we consider those 3 parameters share the same weight. a=b=c=1/3
# correlation_sore = a*similarity + b*timestamp + c*frequency，abc are coefficients.
# timestamp can take into account the time difference:
# The time difference between the (received/sent) messages to be scored and the timestamp of the simulation message.
from datetime import datetime
import time
from llama_local_api import LlamaApi

# every time the LLM generated an influence message, it will output an diffusion_timestamp.
# The

class ScoresUtilities:
    # timestamp = the time that the influence message has been generated.
    # only sent message need to create the time decay
    @staticmethod
    def time_decay():
        # influence message timestamp
        result = LlamaApi.generate_messages_with_timestamps(prompt)
        print(result[0]['timestamp'])
        print(result[0]['message'])

    

