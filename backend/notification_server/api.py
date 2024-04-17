


import requests

from notification_server import api_key


def update_sid(session_id: str, sid: str) -> list[int]:
    r = requests.patch(
        url='nginx://api/users/current/sessions/current',
        headers={'Authorization': api_key},
        data={'socket_id': sid, 'session_id': session_id},
        timeout=10
    )
    assert r.status_code == 200, f'Request of chats failed with HTTP code {r.status_code}. Response: {r.json()}'
    return [int(id_) for id_ in r.json()['data']['chats']]