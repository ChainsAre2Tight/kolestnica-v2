"""Provides a session deleter class"""


from libraries.cache import cache_controller
from libraries.utils.exc import SessionNotFound

from auth_server import db
from auth_server.services.sessions.interfaces import SessionDeleterInterface
from auth_server.helpers.queries_helpers import find_session_by_fingerprint


class SessionDeleter(SessionDeleterInterface):

    @staticmethod
    @cache_controller.remove_from_cache('browser_fingerprint')
    def delete(browser_fingerprint: str) -> None:
        try:
            session = find_session_by_fingerprint(browser_fingerprint=browser_fingerprint)
        except SessionNotFound as e:
            raise SessionNotFound from e

        db.session.delete(session)
        db.session.commit()
