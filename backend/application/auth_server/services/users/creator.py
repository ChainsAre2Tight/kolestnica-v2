"""Conatins user creator"""


from utils.my_dataclasses import CurrentUser
from utils.exc import DuplicateLoginException, DuplicateUsernameException, UserNotFound
from database.models import User, UserLogin

from auth_server.app import db
from auth_server.services.users.interfaces import UserCreatorIntarface
from auth_server.helpers.queries_helpers import find_user_by_username, find_user_login_by_login


class UserCreator(UserCreatorIntarface):

    @staticmethod
    def create(username: str, login: str, pwdh: str) -> CurrentUser:

        # verify there are no duplicates
        try:
            UserCreator._verify_login(login=login)
            UserCreator._verify_username(username=username)
        except (DuplicateLoginException, DuplicateUsernameException) as e:
            raise e

        user, user_login = UserCreator._construct_models(username=username, login=login, pwdh=pwdh)
        UserCreator._add_user_to_database(user=user, user_login=user_login)
        current_user = CurrentUser.from_model(user)

        return current_user


    @staticmethod
    def _construct_models(username: str, login: str, pwdh: str) -> tuple[User, UserLogin]:
        user = User(username=username, alias=username)
        user_login = UserLogin(user=user, login=login, pwdh=pwdh)

        return user, user_login

    @staticmethod
    def _verify_login(login: str) -> None:
        try:
            find_user_login_by_login(login=login)
            raise DuplicateLoginException
        except UserNotFound:
            pass

    @staticmethod
    def _verify_username(username: str) -> None:
        try:
            find_user_by_username(username=username)
            raise DuplicateUsernameException
        except UserNotFound:
            pass

    @staticmethod
    def _add_user_to_database(user: User, user_login: UserLogin) -> None:
        db.session.add_all((user, user_login))
        db.session.commit()
