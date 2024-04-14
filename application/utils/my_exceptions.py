class WrappedFunctionMissingKeyword(BaseException):
    """Raised when wrapped function is missing certain keyword"""

class HTTPException(BaseException):
    """A base class for exceptions that invoke an HTTP error response"""

class UserNotExistsException(HTTPException):
    """Raised when session making a request is terminated or didnt exist in the first place"""

class NoAcccessException(HTTPException):
    """Raised when user atempts to request data he has to right to access"""

class NotPermittedException(HTTPException):
    """Raised when user can access content but cannot perform requested action against it"""

class UserNotFoundException(HTTPException):
    """Raised when specified user cannot be found in the database"""

class SessionNotFound(HTTPException):
    """Raised when session with specified uuid cannot be found in the database"""

class RequestAlreadyFullfilledException(HTTPException):
    """Raised when requested action is not needed as requirement is already fullfilled"""

class DuplicateLoginException(HTTPException):
    """Raised when user attempts to register account to an existing login (email)"""

class DuplicateUsernameException(HTTPException):
    """Raised when user attempts to change his username onto an already taken one"""

class InvalidLoginData(HTTPException):
    """Raised when user provides an invalid login/password pair on login"""

class AlreadyLoggedIn(HTTPException):
    """Raised when user tries to log in to different account from the same session"""

class DeprecatedRefreshToken(HTTPException):
    """Raised when user tries to refresh token pair with an old or invalid refresh token"""
