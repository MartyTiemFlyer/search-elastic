# init_data.py
from elasticsearch import Elasticsearch
from search import init_elasticsearch_data

es = Elasticsearch("http://localhost:9200")
init_elasticsearch_data(es)
