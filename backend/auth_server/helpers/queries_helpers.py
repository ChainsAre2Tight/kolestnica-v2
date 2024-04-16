"""Provides quiries"""

from sqlalchemy.exc import NoResultFound

from libraries.utils.exc import UserNotFound, SessionNotFound
from libraries.database import models
from auth_server import db


def find_user_login_by_login(login: str) -> models.UserLogin:
    try:
        user_login = db.session.query(models.UserLogin).filter(
                models.UserLogin.login == login
            ).one()
    except NoResultFound:
        raise UserNotFound
    return user_login

def find_user_by_username(username: str) -> models.User:
    try:
        user = db.session.query(models.User).filter(
                models.User.username == username
            ).one()
    except NoResultFound:
        raise UserNotFound
    return user

def find_session_by_fingerprint(browser_fingerprint: str) -> models.Session:
    try:
        session = db.session.query(models.Session).filter(
            models.Session.uuid == browser_fingerprint
        ).one()
    except NoResultFound:
        raise SessionNotFound(f"Couldn't find session with fingerprint ({browser_fingerprint})")
    return session
