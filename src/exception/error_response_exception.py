from dataclasses import dataclass


@dataclass
class ErrorResponseException(BaseException):
    message: str = ''
    status_code: int = 500

    def __init__(self, message: str, code: int) -> None:
        super().__init__()
        self.message = message
        self.status_code = code



