"""Provides API reauests for notification server"""


import os

import requests


API_KEY = os.environ.get('API_KEY')


def update_sid(session_id: str, sid: str) -> list[int]:
    """Sends a request to authentification server containing socket id and his parent session data

    Args:
        session_id (str): browser fingerprint
        sid (str): socket id of incoming connection

    Returns:
        list[int]: list of chat ids that user has access to
    """
    print('lox', session_id, sid)
    r = requests.patch(
        url='https://nginx/api/users/current/sessions/current',
        headers={'Authorization': API_KEY},
        json={'socket_id': sid, 'session_id': session_id},
        timeout=10,
        verify=False,
    )
    assert r.status_code == 200, f'Request of chats failed with HTTP code {r.status_code}.\
 Response: {r.json()}'
    return [int(id_) for id_ in r.json()['data']['chats']]
