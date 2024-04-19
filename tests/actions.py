import requests
from requests.cookies import RequestsCookieJar
import hashlib

from json.decoder import JSONDecodeError

from __init__ import host
from shared import UserData, SessionData


def register_user(user: UserData) -> tuple[dict, int]:
    r = requests.post(
        url=f'http://{host}/api/users/',
        json={
            'username': user.username,
            'login': user.login,
            'pwdh': hashlib.md5(user.password.encode()).hexdigest()
        },
        timeout=5
    )
    return r.json(), r.status_code

def login_user(user: UserData, session: SessionData) -> tuple[dict, int, str]:
    r = requests.post(
        url=f'http://{host}/api/users/current/sessions/',
        json={
            'login': user.login,
            'pwdh': hashlib.md5(user.password.encode()).hexdigest(),
            'fingerprint': session.fingerprint
        },
        timeout=5,
    )
    return r.json(), r.status_code, r.cookies.get('r', path='/api/tokens')

def refresh_tokens(refresh_token: str) -> tuple[dict, int, str]:
    cookies = RequestsCookieJar()
    cookies.set('r', refresh_token, path='/api/tokens')
    r = requests.get(
        url=f'http://{host}/api/tokens/',
        timeout=5,
        cookies=cookies
    )
    return r.json(), r.status_code, r.cookies.get('r', path='/api/tokens')

def get_current_user(access: str) -> tuple[dict, int]:
    r = requests.get(
        url=f'http://{host}/api/users/current',
        timeout=5,
        headers={'Authorization': access}
    )
    try:
        j = r.json()
    except JSONDecodeError:
        print('lox', r.text)
    return j, r.status_code

def logout(access: str) -> tuple[dict, int]:
    r = requests.delete(
        url=f'http://{host}/api/users/current/sessions/current',
        timeout=5,
        headers={'Authorization': access}
    )
    try:
        j = r.json()
    except JSONDecodeError:
        print(r.text)
    return j, r.status_code
