"""Provides a session deleter class"""


from utils.exc import SessionNotFound

from auth_server.app import db
from auth_server.actors.sessions.interfaces import SessionDeleterInterface
from auth_server.helpers.queries import find_session_by_fingerprint


class SessionDeleter(SessionDeleterInterface):

    @staticmethod
    def delete(browser_fingerprint: str) -> None:
        try:
            session = find_session_by_fingerprint(browser_fingerprint=browser_fingerprint)
        except SessionNotFound as e:
            raise SessionNotFound from e

        db.session.delete(session)
        db.session.commit()
