import sqlalchemy.exc

import utils.my_exceptions as exc
import utils.my_dataclasses as dataclass
import database.models as models
from user.app import db
import user.tokens as tokens

def create_user(username: str, login: str, pwdh: str) -> dataclass.CurrentUser:
    """
    Attempts to create a user with provided username, login and \
        password hash and returns his data if successful
    
    :params str username: unique username
    :params str login: unique login credential (email)
    :params str pwdh: MD5 hash of user's password

    :returns: dataclass containing all relevant data of the user

    :raises:
        DuplicateLoginException: if there already is an account associated with this login (email)
        DuplicateUsernameException: if there already is an account with specified username
    """
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

def _create_session(user: models.User, sessionId: str) -> models.Session:
    """
    Attempts to create a session for specified user with provided fingerprint

    :params models.User user: user for whom to create session
    :params str sessionId: unique fingerprint of user's browser
    :returns: SQLAlchemy Session models object

    :raises AlreadyLoggedIn: if user has already logged in to a different account from the same device
    """
    # try to create a session for this user with provided fingerprint(uuid)
    try:
        session = models.Session(
            uuid=sessionId,
            user=user
        )
        db.session.add(session)
        db.session.commit()
    
    # if fingerprint isnt unique raise an exception
    # this usually means that user has already logged in to different account from the same device
    except sqlalchemy.exc.IntegrityError:
        db.session.rollback()
        raise exc.AlreadyLoggedIn
    
    return session

def _terminate_sesion(sessionId: str) -> None:
    """
    Attempts to terminate a session associated with provided token data

    :param str sessionId: unique session indentifier

    :raises SessionNotFound: if session with provided data cannot be found
    """
    try:
        session = db.session.query(models.Session).filter(
            models.Session.uuid == sessionId
        ).one()
        db.session.delete(session)
        db.session.commit()
    
    except sqlalchemy.exc.NoResultFound:
        raise exc.SessionNotFound(sessionId)


def login_user(login: str, pwdh: str, uuid: str) -> dataclass.SignedTokenPair:
    """
    Attempts to login user and returns his token pair if successful

    :param str login: user login
    :param str pwdh: MD5 hash of password
    :param str uuid: fingerprint of user's browser

    :returns: dataclass object containing a signed pair of tokens

    :raises InvalidLoginData: if matching login/pwdh pair cannot be found in the database
    """
    
    # try to find a matching login pair in UserLogin model
    try:
        user = db.session.query(models.UserLogin).filter(
            models.UserLogin.login == login,
            models.UserLogin.pwdh == pwdh
        ).one().user
    
    # if it isnt found, raise an exception
    except sqlalchemy.exc.NoResultFound:
        raise exc.InvalidLoginData
    
    try:
        session = _create_session(
            user=user,
            sessionId=uuid
        )
    except exc.AlreadyLoggedIn:
        # if session is a duplicate, terminate the previous one
        _terminate_sesion(uuid)

        session = _create_session(
            user=user,
            sessionId=uuid
        )

    # create and sign a token pair for this session
    token_pair = tokens.create_token_pair(
        sessionId=session.uuid,
        config=tokens.DefaultTokenConfig
    )

    return token_pair

def logout_user(sessionId: str) -> None:
    """
    Attempts to log out user by deleting the session associated with him

    :raises SessionNotFound: if session was already terminated before
    """
    _terminate_sesion(sessionId=sessionId)

def list_active_sessions(sessionId: str) -> list[dataclass.Session]:
    try:
        user = db.session.query(models.Session).\
            filter(models.Session.uuid == sessionId).one().user
    except sqlalchemy.exc.NoResultFound:
        raise exc.UserNotExistsException
    
    return dataclass.convert_model_to_dataclass(
        user.sessions,
        dataclass.Session
    )
