from exception.error_response_exception import ErrorResponseException


class DatabaseNotFoundException(ErrorResponseException):
    def __init__(self, db_id: int):
        super().__init__(f"Database with id = '{db_id}'", 404)
