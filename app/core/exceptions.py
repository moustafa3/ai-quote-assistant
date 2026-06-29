class AppException(Exception):
    """
    Base exception for application-specific errors.
    """


class ResourceNotFoundError(AppException):
    """
    Raised when a requested resource does not exist.
    """