from elasticsearch import Elasticsearch
from pydash import memoize

from .settings import ES_HOST


@memoize
def get_es_client():
    return Elasticsearch(ES_HOST)
