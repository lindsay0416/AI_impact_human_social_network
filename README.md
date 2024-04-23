# AI_impact_human_social_network
RLHF
Reinforcement learning with human feedback

## Setup
### In elasticsearch stores 2 index, called "sent_text_test01" and "received_text_test01"

## 1. Download Database
### 1.1 ElasticSearch 7.7  
- Elasticsearch: https://www.elastic.co/downloads/past-releases/elasticsearch-7-7-0
### 1.2 Kibana 7.7 
- Kibana: https://www.elastic.co/downloads/past-releases/kibana-7-7-0

## 2. Setup the index mapping in elasticsearch
### 2.1. user_sent_messages
Run following script in kibana (http://localhost:5601)

## 3. Start the Elasticsearch egine
* Start elasticsearch:
- `cd /Elasticsearch/elasticsearch-7.7.0/bin`
- `./elasticsearch`

* Start Kibana (UI)
- `cd /Elasticsearch/kibana-7.7.0-darwin-x86_64/bin`
- `./kibana`

### Python version
`python 3.8`

## Details of each python file:

### router.py
* Start ElasticSearch egine

### main.py
* The entrance of the project

### test_main.py
* Test other functions

### graph_data.py
* Stores different hash map structure graph, which represent to the connection of each human or AI in social network

### llm_generate_text.py
* return AI generated text from openai API

### config_manager.py
* This class will handle reading and setting configurations such as API keys from a config file

### es_manager.py
* This class will manage connections and operations related to Elasticsearch.

### test_main.py
This class will use instances of the above classes to perform operations. It acts as the central orchestrator for the application.