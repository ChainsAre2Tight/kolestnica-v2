"""Provides decorators for feed service"""


from functools import wraps

from feed_server import db


def commit(func):
    """Commits changes to database after decorated function is executed"""

    @wraps(func)
    def decorated_function(*args, **kwargs):
        result = func(*args, **kwargs)
        db.session.commit()
        return result
    return decorated_function
