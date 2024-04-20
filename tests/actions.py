
import hashlib
from json.decoder import JSONDecodeError

import requests
from requests.cookies import RequestsCookieJar

from __init__ import host
from shared import UserData, SessionData, ChatData, MessageData


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


def create_chat(chat: ChatData, session: SessionData) -> tuple[dict, int]:
    r = requests.post(
        timeout=5,
        url=f'http://{host}/api/chats/',
        json={'name': chat.name},
        headers={'Authorization': session.access_token}
    )
    try:
        j = r.json()
    except JSONDecodeError:
        print(r.text)
    return j, r.status_code

def get_chat_data(chat: ChatData, session: SessionData) -> tuple[dict, int]:
    r = requests.get(
        timeout=5,
        url=f'http://{host}/api/chats/{chat.id}',
        headers={'Authorization': session.access_token},
    )
    try:
        j = r.json()
    except JSONDecodeError:
        print(r.text)
    return j, r.status_code

def get_chat_members(chat: ChatData, session: SessionData) -> tuple[dict, int]:
    r = requests.get(
        timeout=5,
        url=f'http://{host}/api/chats/{chat.id}/members/',
        headers={'Authorization': session.access_token},
    )
    try:
        j = r.json()
    except JSONDecodeError:
        print(r.text)
    return j, r.status_code

def add_user_to_chat(chat_id: int, target_id: int, session: SessionData) -> tuple[dict, int]:
    r = requests.post(
        timeout=5,
        url=f'http://{host}/api/chats/{chat_id}/members/',
        headers={'Authorization': session.access_token},
        json={'user_id': target_id},
    )
    try:
        j = r.json()
    except JSONDecodeError:
        print(r.text)
    return j, r.status_code

def get_chat_messages(chat: ChatData, session: SessionData) -> tuple[dict, int]:
    r = requests.get(
        timeout=5,
        url=f'http://{host}/api/chats/{chat.id}/messages/',
        headers={'Authorization': session.access_token},
    )
    try:
        j = r.json()
    except JSONDecodeError:
        print(r.text)
    return j, r.status_code

def send_message(chat: ChatData, message: MessageData, session: SessionData) -> tuple[dict, int]:
    r = requests.post(
        timeout=5,
        url=f'http://{host}/api/chats/{chat.id}/messages/',
        headers={'Authorization': session.access_token},
        json={
            'message': {
                'body': message.body,
                'timestamp': message.timestamp
            }
        }
    )
    try:
        j = r.json()
    except JSONDecodeError:
        print(r.text)
    return j, r.status_code
