# This function is about the message retrieve:
# we consider those 3 parameters share the same weight. a=b=c=1/3
# correlation_sore = a*similarity + b*timestamp + c*frequency，abc are coefficients.
# 1.correlation_sore = a*similarity + b*time_decay (ab are coefficients) --> used for retrieve top10 most similarity messages in each user-agent's repository
# 2. trieved message similarity = AVG(top10(similarity))
# 3. INFLUENCE_PROB = \alpha（etrieved message similarity） + (1-\alpha)（user profile (beliefs) similarity）; \alpha=0.5
# timestamp can take into account the time difference:
# The time difference between the (received/sent) messages to be scored and the timestamp of the simulation message.
import time
from llama_local_api import LlamaApi
from sentence_embedding import Text2Vector
import numpy as np
import json

# every time the LLM generated an influence message, it will output an diffusion_timestamp.

class ScoresUtilities:
    # timestamp = the time that the influence message has been generated.
    # only sent message need to create the time decay
    # dm: diffusion message
    # repo: repository message (sent message)
    @staticmethod
    def time_decay(dmTimestamp, repoTimestamp):
        # Ensure both timestamps are not None and are integers
        if dmTimestamp is None or repoTimestamp is None:
            raise ValueError("Timestamps must not be None")
        
        # Calculate time decay
        time_decay = int(dmTimestamp) - int(repoTimestamp)
        return time_decay

    @staticmethod
    def calculate_received_text_scores(es, diffusion_message, prompt, node):
        # Get the generated text and its timestamp
        generated_result = LlamaApi.llama_generate_messages(prompt)
        dmTimestamp = generated_result[0]['timestamp']

        # Get the received text similarity results and their timestamps
        received_results = Text2Vector.received_text_cosine_similarity('received_text_test01', diffusion_message, node, es)

        time_decay_data = []

        # Calculate time decay for received texts
        if received_results:
            for result in received_results:
                repoTimestamp = result[1]
                if repoTimestamp is not None:
                    time_decay_value = ScoresUtilities.time_decay(dmTimestamp, repoTimestamp)
                    probability = 1/2 * int(time_decay_value) + 1/2 * int(result[2])
                    time_decay_data.append({
                        'message': result[0],
                        'time_decay': time_decay_value,
                        'similarity_score': result[2],
                        'probability': probability
                    })
        else:
            print("No received results found to calculate time decay.")

        return time_decay_data

    @staticmethod
    def calculate_sent_text_scores(es, diffusion_message, prompt, node):
        # Get the generated text and its timestamp
        generated_result = LlamaApi.llama_generate_messages(prompt)
        dmTimestamp = generated_result[0]['timestamp']

        # Get the sent text similarity results and their timestamps
        sent_results = Text2Vector.sent_text_cosine_similarity('sent_text_test01', diffusion_message, node, es)

        time_decay_data = []

        # Calculate time decay for sent texts
        # 1/2*time_decay_value + 1/2*similarity = the probability of this message in the reposity be retrieved 
        if sent_results:
            for result in sent_results:
                repoTimestamp = result[1]
                if repoTimestamp is not None:
                    time_decay_value = ScoresUtilities.time_decay(dmTimestamp, repoTimestamp)
                    probability = 1/2 * int(time_decay_value) + 1/2 * int(result[2]) 
                    time_decay_data.append({
                        'message': result[0],
                        'time_decay': time_decay_value,
                        'similarity_score': result[2],
                        'probability': probability
                    })
        else:
            print("No sent results found to calculate time decay.")

        return time_decay_data

    # keep top10 most similar messages.
    @staticmethod
    def calculate_time_decay_and_similarity(es, diffusion_message, prompt, node):
        # TODO: not all the users, just the neigbours. 
        # Calculate scores for received texts
        received_scores = ScoresUtilities.calculate_received_text_scores(es, diffusion_message, prompt, node)

        # Calculate scores for sent texts
        sent_scores = ScoresUtilities.calculate_sent_text_scores(es, diffusion_message, prompt, node)

        # Sort by probability and keep only top 10 records
        top_received_scores = sorted(received_scores, key=lambda x: x['probability'], reverse=True)[:10]
        top_sent_scores = sorted(sent_scores, key=lambda x: x['probability'], reverse=True)[:10]

        # Extract the messages for the top 10 records
        top_received_messages = [score['message'] for score in top_received_scores]
        top_sent_messages = [score['message'] for score in top_sent_scores]

        return {
            'received_scores': top_received_scores,
            'sent_scores': top_sent_scores,
            'received_messages': top_received_messages, # used for generate the prompts
            'sent_messages': top_sent_messages # used for generate the prompts
        }

    @staticmethod
    def read_correlation_data(data):
        # Extract probabilities from received and sent scores
        probabilities = {
            'received_probabilities': [entry['probability'] for entry in data['received_scores']],
            'sent_probabilities': [entry['probability'] for entry in data['sent_scores']]
        }

        # Calculate average similarity scores
        if data['sent_scores']:
            retrieved_sent_message_similarity = sum(entry['similarity_score'] for entry in data['sent_scores']) / len(data['sent_scores'])
        else:
            retrieved_sent_message_similarity = 0

        if data['received_scores']:
            retrieved_received_message_similarity = sum(entry['similarity_score'] for entry in data['received_scores']) / len(data['received_scores'])
        else:
            retrieved_received_message_similarity = 0

        return {
            'probabilities': probabilities,
            'retrieved_sent_message_similarity': retrieved_sent_message_similarity,
            'retrieved_received_message_similarity': retrieved_received_message_similarity
        }
    
    # Compare the Profile similarity.
    # node represents to the users that sending the messages from.
    # TODO: not all the users, just the neigbours. 
        # node find the user profile, 
        # embedding the user profile,  use get_embedding function
        # calculate the user profile similarity,
        # assume the neigbour is N2 and N3, later will be a list of nodes. 
    def profile_similarity(node, user_profile_path='input/user_profile.json'):
        # Load user profiles from JSON file
        with open(user_profile_path, 'r') as file:
            user_profiles = json.load(file)

        # Get the user profile
        user_profile = user_profiles.get(node)
        if not user_profile:
            raise ValueError(f"Profile for node {node} not found.")

        # Create a combined profile string for embedding
        profile_string = f"{user_profile['age']} {user_profile['gender']} {user_profile['description']}"
        
        # Embed the user profile
        user_embedding = Text2Vector.get_embedding(profile_string)

        # Assuming neighbors are N2 and N3 for now
        neighbors = ["N2", "N3"]
        neighbor_embeddings = []
        for neighbor in neighbors:
            neighbor_profile = user_profiles.get(neighbor)
            if neighbor_profile:
                neighbor_profile_string = f"{neighbor_profile['age']} {neighbor_profile['gender']} {neighbor_profile['description']}"
                neighbor_embeddings.append(Text2Vector.get_embedding(neighbor_profile_string))

        # Calculate similarity scores
        similarities = [np.dot(user_embedding, neighbor_embedding) / (np.linalg.norm(user_embedding) * np.linalg.norm(neighbor_embedding)) for neighbor_embedding in neighbor_embeddings]

        return {
            'user_profile': user_profile,
            'similarities': dict(zip(neighbors, similarities))
        }
    #TODO: After change the code to only calculate the correlation_sore for only neigbours, use 3. to get the NFLUENCE_PROB