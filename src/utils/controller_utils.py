import uuid

from exception.error_response_exception import ErrorResponseException
from injector.di.dependency_container import di_container


def exception_handle(func):
    def wrapper(*args, **kw):
        try:
            return func(*args, **kw)
        except ErrorResponseException as e:
            return {'message': e.message}, e.status_code

    wrapper.__name__ = func.__name__
    return wrapper


def require_app_database_session(func):
    def wrapper(self, *args, **kwargs):
        session_id = str(uuid.uuid1())
        di_container.get_app_database_session(session_id)
        try:
            res = func(self, session_id, *args, **kwargs)
        finally:
            di_container.close_app_database_session(session_id)
        return res

    wrapper.__name__ = func.__name__
    return wrapper
