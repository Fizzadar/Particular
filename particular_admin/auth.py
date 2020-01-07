from functools import wraps

from flask import abort, g, session

from particular_admin.app import app
from particular_admin.models.user import User
from particular_admin.util.crypto import generate_key
from particular_admin.util.object import get_object_or_none


@app.before_request
def populate_user():
    email = session.get('email', None)
    session_key = session.get('session_key', None)

    user = None

    if email and session_key:
        user = get_object_or_none(User, email=email, session_key=session_key)

    g.user = user


def get_current_user():
    return g.user


def login_as_user(user):
    user.session_key = generate_key()
    user.save()

    session['email'] = user.email
    session['session_key'] = user.session_key


def logout_current_user():
    for key in session.keys():
        session.pop(key)


def has_user_level(level):
    user = get_current_user()
    return user.level >= level


def require_user_level(level):
    def decorator(func):
        @wraps(func)
        def decorated(*args, **kwargs):
            user = get_current_user()

            if not user:
                abort(401, 'You must be logged in to access this resource.')

            if not has_user_level(level):
                abort(403, (
                    'You cannot access this resource '
                    f'(level={user.level}, needLevel={level}).'
                ))

            return func(*args, **kwargs)
        return decorated
    return decorator


@app.context_processor
def inject_current_user():
    return {
        'current_user': get_current_user(),
        'has_user_level': has_user_level,
    }
