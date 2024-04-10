class UserNotExistsException(BaseException):
    """Raised when session making a request is terminated or didnt exist in the first place"""

class NoAcccessException(BaseException):
    """Raised when user atempts to request data he has to right to access"""
    pass

class NotPermittedException(BaseException):
    """Raised when user can access content but cannot perform requested action against it"""