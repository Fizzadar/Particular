from hashlib import sha1

from pyspider.result import ResultWorker

from particular.settings import ES_INDEX
from particular.util import get_es_client


def _hash(value):
    sha = sha1()
    sha.update(value.encode())
    return sha.hexdigest()


class ElasticsearchIndexer(ResultWorker):
    def on_result(self, task, result):
        url = result['url']
        doc_id = _hash(url)

        es = get_es_client()
        es.index(
            index=ES_INDEX,
            id=doc_id,
            body=result,
        )
