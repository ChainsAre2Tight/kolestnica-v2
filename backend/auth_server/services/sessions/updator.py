"""Provides session updator class"""

from libraries.utils.exc import SessionNotFound

from auth_server import db
from auth_server.services.sessions.interfaces import SessionUpdaterIntarface
from auth_server.helpers.queries_helpers import find_session_by_fingerprint


class SessionUpdator(SessionUpdaterIntarface):

    @staticmethod
    def update_refresh_token(browser_fingerprint: str, new_refresh_token: str) -> None:
        try:
            session = find_session_by_fingerprint(browser_fingerprint=browser_fingerprint)
        except SessionNotFound as e:
            raise SessionNotFound from e

        session.refresh_token = new_refresh_token
        db.session.commit()

    @staticmethod
    def update_socket_id(session_id: int, new_socker_id: str) -> None:
        raise NotImplementedError('Socket id updator is yet to be implemented')
