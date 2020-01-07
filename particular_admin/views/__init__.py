from flask import render_template, send_from_directory

from particular.util import get_es_client
from particular_admin.app import app
from particular_admin.models.website import Website
from particular_admin.settings import ES_INDEX, PARTICULAR_STATIC_DIR


@app.route('/', methods=('GET',))
def get_index():
    website_count = Website.query.count()
    page_count = get_es_client().count(
        index=ES_INDEX,
    )['count']

    return render_template(
        'index.html',
        website_count=website_count,
        page_count=page_count,
    )


@app.route('/about', methods=('GET',))
def get_about():
    return render_template('about.html')


@app.route('/particular_static/<path:filename>', methods=('GET',))
def particular_static(filename):
    return send_from_directory(PARTICULAR_STATIC_DIR, filename)
