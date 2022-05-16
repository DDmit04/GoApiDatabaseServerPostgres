import random
import string

from sqlalchemy import select, delete, update, insert

from App.tables.DatabaseTable import database
from App.utils.DbUtils import transactional_class_method


class LocalDatabaseRepository:

    @transactional_class_method
    def get_databases_info(self, session):
        select_query = select(database)
        query_res = session.execute(select_query).all()
        res = [dict(db) for db in query_res]
        return res

    @transactional_class_method
    def add_database_info(self, session, username, new_db_name, real_id, size):
        insert_query = insert(database).values(
            username=username,
            db_id=real_id,
            db_size=size,
            db_name=new_db_name
        )
        session.execute(insert_query)

    @transactional_class_method
    def remove_database_info(self, session, db_id):
        deleteDbInfoQuery = delete(database).where(database.c.db_id == db_id)
        session.execute(deleteDbInfoQuery)

    @transactional_class_method
    def get_database_info(self, session, db_id):
        select_query = select(database).where(database.c.db_id == db_id)
        query_res = session.execute(select_query).all()
        info_res = query_res.first()
        return dict(info_res)

    @transactional_class_method
    def update_database_size_info(self, session, db_id, new_size):
        update_query = update(database).where(database.c.db_id == db_id).values(db_size=new_size)
        session.execute(update_query)

    @transactional_class_method
    def is_database_exists_by_db_id(self, session, db_id):
        query = select(database).where(database.c.db_id == db_id)
        res = session.execute(query)
        db_res = res.first()
        return db_res is not None

    @transactional_class_method
    def get_database_by_db_id(self, session, db_id):
        query = select(database).where(database.c.db_id == db_id)
        res = session.execute(query)
        db_res = res.first()
        if db_res is None:
            return None
        return dict(db_res)

    @transactional_class_method
    def get_database_by_name(self, session, db_name):
        query = select(database.c.db_id).where(database.c.db_name == db_name)
        res = session.execute(query)
        db = res.first()
        if db is None:
            return None
        return dict(db)

    @transactional_class_method
    def get_database_by_username(self, session, username):
        query = select(database.c.db_id).where(database.c.username == username)
        res = session.execute(query)
        db = res.first()
        if db is None:
            return None
        return dict(db)

    @transactional_class_method
    def get_new_username(self, session, name_length):
        username = ''.join(random.choices(string.ascii_lowercase, k=name_length))
        user_exists = self.get_database_by_username(session, username) is not None
        while user_exists:
            username = random.choices(string.ascii_lowercase)
            user_exists = self.get_database_by_username(session, username) is not None
        return username

    @transactional_class_method
    def get_new_database_name(self, session, name_length):
        db_name = ''.join(random.choices(string.ascii_lowercase, k=name_length))
        db_exists = self.get_database_by_name(session, db_name) is not None
        while db_exists:
            db_name = random.choices(string.ascii_lowercase)
            db_exists = self.get_database_by_name(session, db_name) is not None
        return db_name
