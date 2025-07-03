
class VxException(Exception):
    def __init__(self, message: str):
        self.message = message

    def print_message(self):
        print(str(self))

    def __str__(self):
        return self.message

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
