from flask import abort
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound


def get_object_or_none(object_class, **filters):
    try:
        return object_class.query.filter_by(**filters).one()
    except (NoResultFound, MultipleResultsFound):
        return None


def get_object_or_404(object_class, **filters):
    if 'hashed_id' in filters:
        filters['id'] = object_class.hash_to_id(filters.pop('hashed_id'))

    try:
        obj = object_class.query.filter_by(**filters).one()
    except NoResultFound:
        abort(404, f'No {object_class.__name__} found with given filters.')
    except MultipleResultsFound:
        abort(400, f'Multiple {object_class.__name__} found with given filters.')

    return obj
