from elasticsearch import Elasticsearch

class ESManager:
    def __init__(self, host_url):
        self.es = Elasticsearch(host_url)

    def is_connected(self):
        return self.es.ping()

    def index(self, index_name, document_body):
        return self.es.index(index=index_name, document=document_body)
