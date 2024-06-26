


from typing import Literal
from functools import wraps

import requests
from celery import states
from celery.exceptions import Ignore

from celery_worker import api_key


HOST = 'https://kolestnica.ru/notifications'


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
        'headers': {'Authorization': api_key, 'Content-Type': 'application/json'},
        'timeout': 10,
        'verify': False,
        'allow_redirects': False,
    }
    if json:
        options['json'] = json

    match header:
        case 'POST':
            action = requests.post
        case 'PATCH':
            action = requests.patch
        case 'DELETE':
            action = requests.delete
        case _:
            raise ValueError(f'Unsupported request type "{header}"')

    r = action(**options)

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
