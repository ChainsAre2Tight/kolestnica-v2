"""Contains user creator"""

from sqlalchemy.exc import IntegrityError

from libraries.utils.my_dataclasses import Session as d_Session
from libraries.utils.exc import InvalidLoginData, AlreadyLoggedIn, UserNotFound
from libraries.database.models import User, UserLogin, Session

from auth_server import db
from auth_server.services.sessions.interfaces import SessionCreatorInterface
from auth_server.helpers.queries_helpers import find_user_login_by_login


class SessionCreator(SessionCreatorInterface):

    @staticmethod
    def create(login: str, pwdh: str, browser_fingerprint: str) -> d_Session:
        user = SessionCreator._login(login=login, pwdh=pwdh)
        session = SessionCreator._create_session(user=user, browser_fingerprint=browser_fingerprint)

        session_data = d_Session.from_model(session)
        return session_data


    @staticmethod
    def _login(login: str, pwdh: str) -> UserLogin:
        try:
            user_login = find_user_login_by_login(login=login)
            if user_login.pwdh != pwdh:
                raise InvalidLoginData
        except UserNotFound:
            raise InvalidLoginData

        return user_login.user

    @staticmethod
    def _create_session(user: User, browser_fingerprint: str) -> Session:
        try:
            session = Session(
                uuid=browser_fingerprint,
                user=user
            )
            db.session.add(session)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise AlreadyLoggedIn
        return session
