# This function is about the message retrieve:
# we consider those 3 parameters share the same weight. a=b=c=1/3
# correlation_sore = a*similarity + b*timestamp + c*frequency，abc are coefficients.
# 1.correlation_sore = a*similarity + b*time_decay (ab are coefficients) --> used for retrieve top10 most similarity messages in each user-agent's repository
# 2. trieved message similarity = AVG(top10(similarity))
# 3. NFLUENCE_PROB = \alpha（etrieved message similarity） + (1-\alpha)（user profile (beliefs) similarity）; \alpha=0.5
# timestamp can take into account the time difference:
# The time difference between the (received/sent) messages to be scored and the timestamp of the simulation message.
import time
from llama_local_api import LlamaApi
from sentence_embedding import Text2Vector

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
        generated_result = LlamaApi.generate_messages_with_timestamps(prompt)
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
                    probability = 1/3 * int(time_decay_value) + 1/3 * int(result[2])
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
        generated_result = LlamaApi.generate_messages_with_timestamps(prompt)
        dmTimestamp = generated_result[0]['timestamp']

        # Get the sent text similarity results and their timestamps
        sent_results = Text2Vector.sent_text_cosine_similarity('sent_text_test01', diffusion_message, node, es)

        time_decay_data = []

        # Calculate time decay for sent texts
        if sent_results:
            for result in sent_results:
                repoTimestamp = result[1]
                if repoTimestamp is not None:
                    time_decay_value = ScoresUtilities.time_decay(dmTimestamp, repoTimestamp)
                    probability = 1/3 * int(time_decay_value) + 1/3 * int(result[2])
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
        # Calculate scores for received texts
        received_scores = ScoresUtilities.calculate_received_text_scores(es, diffusion_message, prompt, node)

        # Calculate scores for sent texts
        sent_scores = ScoresUtilities.calculate_sent_text_scores(es, diffusion_message, prompt, node)

        # Sort by probability and keep only top 10 records
        top_received_scores = sorted(received_scores, key=lambda x: x['probability'], reverse=True)[:10]
        top_sent_scores = sorted(sent_scores, key=lambda x: x['probability'], reverse=True)[:10]

        return {
            'received_scores': top_received_scores,
            'sent_scores': top_sent_scores
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
            etrieved_sent_message_similarity = sum(entry['similarity_score'] for entry in data['sent_scores']) / len(data['sent_scores'])
        else:
            etrieved_sent_message_similarity = 0

        if data['received_scores']:
            etrieved_received_message_similarity = sum(entry['similarity_score'] for entry in data['received_scores']) / len(data['received_scores'])
        else:
            etrieved_received_message_similarity = 0

        return {
            'probabilities': probabilities,
            'etrieved_sent_message_similarity': etrieved_sent_message_similarity,
            'etrieved_received_message_similarity': etrieved_received_message_similarity
        }
    
    #TODO: Compare the Profile similarity.