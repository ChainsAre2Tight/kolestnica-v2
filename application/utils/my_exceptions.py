class UserNotExistsException(BaseException):
    """Raised when session making a request is terminated or didnt exist in the first place"""

class NoAcccessException(BaseException):
    """Raised when user atempts to request data he has to right to access"""

class NotPermittedException(BaseException):
    """Raised when user can access content but cannot perform requested action against it"""

class UserNotFoundException(BaseException):
    """Raised when specified user cannot be found in the database"""

class SessionNotFound(BaseException):
    """Raised when session with specified uuid cannot be found in the database"""

class RequestAlreadyFullfilledException(BaseException):
    """Raised when requested action is not needed as requirement is already fullfilled"""

class DuplicateLoginException(BaseException):
    """Raised when user attempts to register account to an existing login (email)"""

class DuplicateUsernameException(BaseException):
    """Raised when user attempts to change his username onto an already taken one"""

class InvalidLoginData(BaseException):
    """Raised when user provides an invalid login/password pair on login"""

class AlreadyLoggedIn(BaseException):
    """Raised when user tries to log in to different account from the same session"""