import sqlalchemy.exc

import utils.my_exceptions as exc
import utils.my_dataclasses as dataclass
import database.models as models
from user.app import db

def create_user(username: str, login: str, pwdh: str) -> dataclass.CurrentUser:
    new_user = models.User(
        username=username,
        alias=username,
    )

    new_login = models.UserLogin(
        user=new_user,
        login=login,
        pwdh=pwdh
    )

    try:
        # try to find an existing user with such login
        db.session.query(models.UserLogin).filter(
            models.UserLogin.login == login
        ).one()
        raise exc.DuplicateLoginException
    except sqlalchemy.exc.NoResultFound:
        pass

    try:
        # try to find an exisitng user with the same username
        db.session.query(models.User).filter(
            models.User.username == username
        ).one()
        raise exc.DuplicateUsernameException
    except sqlalchemy.exc.NoResultFound:
        pass

    # TODO check if no user has the same password :)

    # add new user assuming there will be no duplicate data
    db.session.add_all((new_user, new_login))
    db.session.commit()

    return dataclass.CurrentUser.from_model(new_user)