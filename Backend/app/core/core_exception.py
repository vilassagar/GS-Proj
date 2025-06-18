
class VxException(Exception):
    def __init__(self, message: str):
        self.message = message

    def print_message(self):
        print(str(self))

    def __str__(self):
        return self.message


class UnauthorizedException(VxException):
    def __int__(self, message: str):
        super().__init__(message)
