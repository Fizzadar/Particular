from flask import Flask, render_template, request

from particular import settings
from particular.settings import DEBUG, ES_INDEX, SECRET_KEY
from particular.util import get_es_client

app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY


@app.context_processor
def inject_settings():
    return {
        'settings': settings,
    }


@app.route('/', methods=('GET',))
def get_index():
    query = request.args.get('q')
    if not query:
        return render_template('index.html', is_index=True)

    return do_search(query)


def do_search(query):
    es = get_es_client()

    results = es.search(
        index=ES_INDEX,
        body={
            'query': {
                'simple_query_string': {
                    'query': query,
                    'fields': [
                        'title^5', 'title_page^5', 'title_rss^5',
                        'description^3',
                        'text', 'authors',
                    ],
                    'default_operator': 'AND',
                },
            },
            'aggregations': {
                'domains': {
                    'terms': {
                        'field': 'source_domain',
                    },
                },
            },
        },
    )

    results_total = results['hits']['total']['value']
    domains = results['aggregations']['domains']['buckets']

    def make_result(result):
        return {
            'title': result['title'],
            'domain': result['source_domain'],
            'url': result['url'],
            'excerpt': result['text'],
        }

    results = [make_result(hit['_source']) for hit in results['hits']['hits']]

    return render_template(
        'index.html',
        results=results,
        results_total=results_total,
        domains=domains,
    )
