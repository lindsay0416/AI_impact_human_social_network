# from llm_generate_text import GenerateText
from sentence_embedding import Text2Vector
import time

class ElasticSeachStore():
    @staticmethod
    def add_received_record(index_name, document_body, es):
        received_text = document_body.get('received_text')
        if received_text:
            document_body['received_text_vector'] = Text2Vector.get_embedding(received_text)
        response = es.index(index=index_name, document=document_body)
        return response  # Return raw response or process as needed

    @staticmethod
    def add_sent_record(index_name, document_body, es):
        sent_text = document_body.get('sent_text')
        if sent_text:
            document_body['sent_text_vector'] = Text2Vector.get_embedding(sent_text)
        response = es.index(index=index_name, document=document_body)
        return response  # Return raw response or process as needed

    @staticmethod
    def add_record_to_elasticsearch(node, connected_node, text, weight, is_received, es):
        # current_timestamp = time.time_ns()
        document_body = {
            "node": connected_node if is_received else node,
            "from": node if is_received else None,
            "to": connected_node if not is_received else None,
            "received_text": text if is_received else None,
            "sent_text": text if not is_received else None,
            "received_text_weight": str(weight) if is_received else None,
            "timestamp": time.time_ns(),
        }
        document_body = {k: v for k, v in document_body.items() if v is not None}
        index_name = "received_text_test01" if is_received else "sent_text_test01"

        # Decide whether to add a received or sent record based on is_received flag
        if is_received:
            response = ElasticSeachStore.add_received_record(index_name, document_body, es)
        else:
            response = ElasticSeachStore.add_sent_record(index_name, document_body, es)

        # Print or log the response as needed
        print(f"{'Received' if is_received else 'Sent'}: {document_body}")
        print("Response from Elasticsearch:", response)
        return response  # Return raw response or process as needed