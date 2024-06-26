"""Contains session reader"""


from libraries.database.models import Session
from libraries.utils.exc import SessionNotFound

from auth_server.services.sessions.interfaces import SessionReaderIntarface
from auth_server.helpers.queries_helpers import find_session_by_fingerprint


class SessionReader(SessionReaderIntarface):

    @staticmethod
    def read(browser_fingerprint: str) -> Session:
        try:
            session = find_session_by_fingerprint(browser_fingerprint=browser_fingerprint)
        except SessionNotFound as e:
            raise SessionNotFound from e

        return session
