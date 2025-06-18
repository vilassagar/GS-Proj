class CommonException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class UnauthorizedException(CommonException):
    def __init__(self, message):
        super().__init__(message)


class InvalidRequestException(CommonException):
    def __init__(self, message):
        super().__init__(message)


class NotFoundException(CommonException):
    def __init__(self, message):
        super().__init__(message)


class ConflictException(CommonException):
    def __init__(self, message):
        super().__init__(message)


class NotAcceptable(CommonException):
    def __init__(self, message):
        super().__init__(message)
