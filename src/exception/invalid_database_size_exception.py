from exception.error_response_exception import ErrorResponseException


class InvalidDatabaseSizeException(ErrorResponseException):

    def __init__(self, db_id: int, new_size: int):
        super().__init__(f"Database with id = "
                         f"'{db_id}' can't set size = '"
                         f"{new_size}'", 403)
