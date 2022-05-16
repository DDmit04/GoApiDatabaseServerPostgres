import sqlalchemy.orm.session


def transactional_class_method(f):
    def wrapper(self, session_factory, *args, **kw):
        if isinstance(session_factory, sqlalchemy.orm.session.sessionmaker):
            with session_factory.begin() as session:
                try:
                    res = f(self, session, *args, **kw)
                except Exception as e:
                    session.rollback()
                    raise e
                return res
        elif isinstance(session_factory, sqlalchemy.orm.session.Session):
            res = f(self, session_factory, *args, **kw)
            return res
        else:
            raise f"First argument in class method {f.__name__} isn't sessionmaker or session!"

    return wrapper


def transactional(f):
    def wrapper(session_factory, *args, **kw):
        if type(session_factory) == sqlalchemy.orm.session.sessionmaker:

            with session_factory.begin() as session:
                try:
                    res = f(session, *args, **kw)
                except Exception as e:
                    session.rollback()
                    raise e
                return res
        elif type(session_factory) == sqlalchemy.orm.session.Session:
            res = f(session_factory, *args, **kw)
            return res
        else:
            raise f"First argument in class method {f.__name__} isn't session_maker or session!"

    return wrapper
