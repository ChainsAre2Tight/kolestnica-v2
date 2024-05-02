


from typing import Literal
from functools import wraps

import requests
from celery import states
from celery.exceptions import Ignore

from celery_worker import api_key


HOST = 'http://nginx/notifications'


class TaskFailure(Exception):
    pass


def send_request(
        header: Literal['POST', 'PATCH', 'DELETE'],
        path: str,
        json: dict = None,
        success_code: int = 200
    ) -> None:

    options = {
        'url': f'{HOST}{path}',
        'headers': {'Authentification': api_key},
        'timeout': 10
    }
    if json:
        options['json'] = json

    match header:
        case 'POST':
            r = requests.post(**options)
        case 'PATCH':
            r = requests.patch(**options)
        case 'DELETE':
            r = requests.delete(**options)
        case _:
            raise ValueError(f'Unsupported request type "{header}"')

    if r.status_code != success_code:
        raise TaskFailure(r.text)


def fail_on_exception(func):

    @wraps(func)
    def decorated_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TaskFailure as e:
            kwargs['self'].update_state(
                state=states.FAILURE,
                meta=str(e)
            )
            raise Ignore()
    return decorated_function
