

from utils.my_dataclasses import Session
from utils.exc import SessionNotFound

from auth_server.actors.sessions.interfaces import SessionReaderIntarface
from auth_server.helpers.queries import find_session_by_fingerprint



class SessionReader(SessionReaderIntarface):

    @staticmethod
    def read(browser_fingerprint: str) -> Session:
        try:
            session = find_session_by_fingerprint(browser_fingerprint=browser_fingerprint)
        except SessionNotFound as e:
            raise SessionNotFound from e

        session_data = Session.from_model(session)
        return session_data
