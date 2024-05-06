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
    
    # Compare with the diffusion message, retrieve the top 10 similar messages in the "received_text_test01"
    def received_text_cosine_similarity(index_name, diffusion_message, es):
        # Convert diffusion_message to a vector
        query_vector = Text2Vector.get_embedding(diffusion_message)

        # Define the Elasticsearch query
        script_query = {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": """
                    if (!doc['received_text_vector'].empty) {
                        return cosineSimilarity(params.query_vector, 'received_text_vector') + 1.0;
                    } else {
                        return 0.0; // Default score if vector is missing
                    }
                    """,
                    "params": {"query_vector": query_vector}  # Correctly use the list without converting
                }
            }
        }

        # Perform the search
        try:
            response = es.search(index=index_name, body={"query": script_query, "size": 10})
            return [(hit['_source']['received_text'], hit['_score']) for hit in response['hits']['hits']]
        except Exception as e:
            print("Error during search:", e)
            return []
        

    def sent_text_cosine_similarity(index_name, diffusion_message, es):
        # Embed the diffusion message into a vector using a pre-trained model
        query_vector = Text2Vector.get_embedding(diffusion_message)

        # Elasticsearch script to compute cosine similarity
        script_query = {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": """
                    if (!doc['sent_text_vector'].empty) {
                        return cosineSimilarity(params.query_vector, 'sent_text_vector') + 1.0;
                    } else {
                        return 0.0;  // Default score if vector is missing
                    }
                    """,
                    "params": {"query_vector": query_vector}  # Query vector already in list format
                }
            }
        }

        # Execute the search query
        try:
            response = es.search(index=index_name, body={"query": script_query, "size": 10})
            return [(hit['_source']['sent_text'], hit['_score']) for hit in response['hits']['hits']]
        except Exception as e:
            print("Error during search:", e)
            return []


    def get_messages_from_list(results):
            # Extracting text from each tuple
        texts = [text for text, score in results]
        return texts
    
    # # Received text vector
    # @staticmethod
    # def received_text_cosine_similarity(index_name, query_vector, es):
    #     script_query = {
    #     "script_score": {
    #         "query": {"match_all": {}},
    #         "script": {
    #             "source": """
    #             if (!doc['received_text_vector'].empty) {
    #                 return cosineSimilarity(params.query_vector, 'received_text_vector') + 1.0;
    #             } else {
    #                 return 0.0; // Default score if vector is missing
    #             }
    #             """,
    #             "params": {"query_vector": query_vector}
    #             }
    #         }
    #     }
    #     try:
    #         response = es.search(index=index_name, body={"query": script_query, "size": 10})
    #         return response
    #     except RequestError as e:
    #         print("RequestError occurred:", e.info)
    #         raise
    
    # # Sent text vector
    # @staticmethod
    # def sent_text_cosine_similarity(index_name, query_vector, es):   
    #     script_query = {
    #     "script_score": {
    #         "query": {"match_all": {}},
    #         "script": {
    #             "source": "cosineSimilarity(params.query_vector, 'sent_text_vector') + 1.0",
    #             "params": {"query_vector": query_vector}
    #             }
    #         }
    #     }
    #     try:
    #         response = es.search(index=index_name, body={"query": script_query, "size": 1})
    #         return response
    #     except RequestError as e:
    #         print("RequestError occurred:", e.info)
    #         raise

    # # return the similarity score
    # @staticmethod
    # def get_similarity_score(SimilarityResp):
    #     scores = []
    #     for hit in SimilarityResp['hits']['hits']:
    #         score = hit['_score'] - 1.0  # Subtracting 1.0 because we added 1.0 in the script
    #         scores.append(score)
    #     return scores
        
    # # Test, return the detail of an index.
    # @staticmethod
    # def test_script(index_name, es):
    #     script_query = {
    #     "script_score": {
    #         "query": {"match_all": {}},
    #         "script": {
    #             "source": "1"  # Just returns a constant score
    #         }
    #     }
    # }
    #     response = es.search(index=index_name, body={"query": script_query, "size": 10})
    #     return response

            


 