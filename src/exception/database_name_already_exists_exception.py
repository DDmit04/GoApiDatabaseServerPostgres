from exception.error_response_exception import ErrorResponseException


class DatabaseNameAlreadyExistsException(ErrorResponseException):

    def __init__(self, db_name: int) -> None:
        super().__init__(f"Database with name = '{db_name}' already exists",
                         409)

