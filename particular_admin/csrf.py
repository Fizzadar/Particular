from functools import wraps

from flask import abort, request, session
from jinja2 import Markup

from particular_admin.app import app
from particular_admin.util.crypto import generate_key
from particular_admin.util.request import get_form_data


def verify_csrf(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        if request.method == 'POST':
            token = session.get('_csrf_token')

            if not token or token != get_form_data().get('csrf_token'):
                abort(400, 'Invalid and/or missing CSRF token.')

        return func(*args, **kwargs)
    return decorator


def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = generate_key()
    return session['_csrf_token']


def generate_csrf_input():
    token = generate_csrf_token()

    return Markup(
        '<input type="hidden" name="csrf_token" value="{0}" />'.format(
            token,
        ),
    )


@app.context_processor
def inject_csrf_functions():
    return {
        'csrf_token': generate_csrf_token,
        'csrf_input': generate_csrf_input,
    }
