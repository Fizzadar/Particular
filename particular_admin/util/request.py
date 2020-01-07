from functools import wraps

from flask import abort, request


def get_form_data():
    return {
        key: value[0] if len(value) == 1 else value
        for key, value in request.form.lists()
    }


def pass_request_data(keys, required=True):
    def decorator(func):
        @wraps(func)
        def decorated(*args, **kwargs):
            request_data = get_form_data()

            for key in keys:
                data = request_data.get(key)
                if required and not data:
                    abort(400, f'Missing data: {key}')
                kwargs[key] = data

            return func(*args, **kwargs)
        return decorated
    return decorator
