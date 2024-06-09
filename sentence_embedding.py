# Those functions are not in use, atm
from sentence_transformers import SentenceTransformer
# from elasticsearch import RequestError

class Text2Vector:
    
    @staticmethod
    def get_embedding(text):
        # Initialize the Sentence Transformer model
        model = SentenceTransformer('all-MiniLM-L6-v2')
        # Generate the embedding for the text
        embedding = model.encode(text).tolist()
        return embedding
    
    @staticmethod
    def build_script_query(query_vector, vector_field, node):
        # Define the Elasticsearch query
       return {
            "script_score": {
                "query": {
                    "bool": {
                        "must": [
                            {"match": {"node": node}}
                        ]
                    }
                },
                "script": {
                    "source": f"""
                        if (!doc['{vector_field}'].empty) {{
                            return cosineSimilarity(params.query_vector, '{vector_field}') + 1.0;
                        }} else {{
                            return 0.0; // Default score if vector is missing
                        }}
                    """,
                    "params": {"query_vector": query_vector}
                }
            }
        }
    
    @staticmethod
    def query_elasticsearch(index_name, script_query, es):
        # Perform the search
        try:
            response = es.search(index=index_name, body={"query": script_query, "size": 10})
            return [(hit['_source'], hit['_score']) for hit in response['hits']['hits']]
        except Exception as e:
            print("Error during search:", e)
            return []
        
    @staticmethod
    def received_text_cosine_similarity(index_name, diffusion_message, node, es):
        # Convert diffusion_message to a vector
        query_vector = Text2Vector.get_embedding(diffusion_message)

        # Build the script query
        script_query = Text2Vector.build_script_query(query_vector, 'received_text_vector', node)

        # Perform the search
        results = Text2Vector.query_elasticsearch(index_name, script_query, es)
        return [(hit.get('received_text'), hit.get('timestamp'), score) for hit, score in results]

    @staticmethod
    def sent_text_cosine_similarity(index_name, diffusion_message, node, es):
        # Embed the diffusion message into a vector using a pre-trained model
        query_vector = Text2Vector.get_embedding(diffusion_message)

        # Build the script query
        script_query = Text2Vector.build_script_query(query_vector, 'sent_text_vector', node)

        # Execute the search query
        results = Text2Vector.query_elasticsearch(index_name, script_query, es)
        return [(hit.get('sent_text'), hit.get('timestamp'), score) for hit, score in results]

    @staticmethod
    def get_messages_from_list(results):
        # Extracting text and timestamp from each tuple
        texts = [{'message': text, 'timestamp': timestamp, 'score':score} for text, timestamp, score in results]
        return texts
            


 