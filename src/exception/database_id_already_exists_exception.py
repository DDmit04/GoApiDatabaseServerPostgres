from exception.error_response_exception import ErrorResponseException


class DatabaseIdAlreadyExistsException(ErrorResponseException):

    def __init__(self, db_id: int) -> None:
        super().__init__(f"Database with id = '{db_id}' already exists",
                         409)

