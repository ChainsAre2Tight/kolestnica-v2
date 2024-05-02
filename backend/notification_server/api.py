"""Provides API reauests for notification server"""


import requests

from notification_server import api_key


def update_sid(session_id: str, sid: str) -> list[int]:
    """Sends a request to notification server containing socket id and his parent session data

    Args:
        session_id (str): browser fingerprint
        sid (str): socket id of incoming connection

    Returns:
        list[int]: list of chat ids that user has access to
    """
    
    print('lox', session_id, sid)
    r = requests.patch(
        url='http://nginx/api/users/current/sessions/current',
        headers={'Authorization': api_key},
        json={'socket_id': sid, 'session_id': session_id},
        timeout=10
    )
    assert r.status_code == 200, f'Request of chats failed with HTTP code {r.status_code}.\
 Response: {r.json()}'
    return [int(id_) for id_ in r.json()['data']['chats']]
