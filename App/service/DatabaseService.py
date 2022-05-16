from sqlalchemy_utils import database_exists, create_database, drop_database

import Config
from App.utils.DbConnectionUtils import get_db_engine_by_name, get_user_session_factory
from App.controller.dto.DatabaseInfoDto import DatabaseInfoDto
from App.controller.dto.DatabaseStatsDto import DatabaseStatsDto
from App.exception.DatabaseAlreadyExistsException import DatabaseAlreadyExistsException
from App.exception.DatabaseNotFoundException import DatabaseNotFoundException
from App.exception.InvalidDatabaseSizeException import InvalidDatabaseSizeException


class DatabaseService:

    def __init__(self, local_db_repo, target_db_repo) -> None:
        super().__init__()
        self.local_db_repo = local_db_repo
        self.target_db_repo = target_db_repo

    def exec_user_query(self, session_factory, real_db_id, query):
        db_to_query = self.local_db_repo.get_database_by_db_id(session_factory, real_db_id)
        if db_to_query is not None:
            db_name = db_to_query['db_name']
            db_engine_to_query = get_db_engine_by_name(Config.db_config, db_name)
            target_db_session_factory = get_user_session_factory(db_engine_to_query)
            return self.target_db_repo.exec_target_user_query(target_db_session_factory, query)
        else:
            raise DatabaseNotFoundException();

    def get_local_databases_info(self, session_factory):
        return self.local_db_repo.get_databases_info(session_factory)

    def create_user_database(self, session_factory, password, db_size, real_db_id):
        db_exists = self.local_db_repo.is_database_exists_by_db_id(session_factory, real_db_id)
        if not db_exists:
            db_name = self.local_db_repo.get_new_database_name(session_factory, Config.db_config['DB_NAME_LENGTH'])
            try:
                new_db_engine = get_db_engine_by_name(Config.db_config, db_name)
                is_real_db_exists = database_exists(new_db_engine.url)
                if not is_real_db_exists:
                    create_database(new_db_engine.url)
                    try:
                        new_username = self.local_db_repo.get_new_username(session_factory,
                                                                           Config.db_config['DB_USERNAME_LENGTH'])
                        self.local_db_repo.add_database_info(session_factory, new_username, db_name, real_db_id,
                                                             db_size)
                        new_db_engine = get_db_engine_by_name(Config.db_config, db_name)
                        new_db_session_factory = get_user_session_factory(new_db_engine)
                        self.target_db_repo.init_new_database(new_db_session_factory, new_username, password, db_size)
                    except Exception as e:
                        self.local_db_repo.remove_database_info(session_factory, real_db_id)
                        drop_database(new_db_engine.url)
                        raise e
                    return DatabaseInfoDto(db_name, new_username)
                else:
                    raise DatabaseAlreadyExistsException()
            finally:
                new_db_engine.dispose()
        else:
            raise DatabaseNotFoundException()

    def drop_db(self, session_factory, db_id):
        db_to_drop = self.local_db_repo.get_database_by_db_id(session_factory, db_id)
        if db_to_drop is not None:
            db_name = db_to_drop['db_name']
            db_engine_to_drop = get_db_engine_by_name(Config.db_config, db_name)
            drop_database(db_engine_to_drop.url)
            deleted_database_info = self.local_db_repo.get_database_info(session_factory, db_id)
            self.local_db_repo.remove_database_info(session_factory, db_id)
            return deleted_database_info
        else:
            raise DatabaseNotFoundException()

    def reset_database(self, session_factory, db_id, password):
        deleted_database_info = self.drop_db(session_factory, db_id)
        if deleted_database_info is not None:
            deleted_db_size = deleted_database_info['db_size']
            return self.create_user_database(session_factory, password, deleted_db_size, db_id)
        raise DatabaseNotFoundException()

    def update_database_size(self, session_factory, db_id, new_size):
        db_to_update = self.local_db_repo.get_database_by_db_id(session_factory, db_id)
        if db_to_update is not None:
            db_name = db_to_update['db_name']
            target_db_engine = get_db_engine_by_name(Config.db_config, db_name)
            try:
                target_db_session_factory = get_user_session_factory(target_db_engine)
                current_size = self.target_db_repo.get_database_stats(target_db_session_factory)['current_bytes']
                is_valid = current_size < new_size
                if is_valid:
                    self.local_db_repo.update_database_size_info(session_factory, db_id, new_size)
                    self.target_db_repo.update_database_size(target_db_session_factory, new_size)
                    return True
                else:
                    raise InvalidDatabaseSizeException()
            finally:
                target_db_engine.dispose()
        else:
            raise DatabaseNotFoundException()

    def update_database_password(self, session_factory, db_id, new_password):
        db_to_update = self.local_db_repo.get_database_by_db_id(session_factory, db_id)
        if db_to_update is not None:
            username = db_to_update['username']
            self.target_db_repo.update_user_password(session_factory, username, new_password)
            return True
        else:
            raise DatabaseNotFoundException()

    def get_target_database_stats(self, session_factory, db_id):
        target_db = self.local_db_repo.get_database_by_db_id(session_factory, db_id)
        if target_db is not None:
            db_name = target_db['db_name']
            target_db_engine = get_db_engine_by_name(Config.db_config, db_name)
            try:
                target_db_session_factory = get_user_session_factory(target_db_engine)
                stats = self.target_db_repo.get_database_stats(target_db_session_factory)
                statsDto = DatabaseStatsDto(stats['fill_percent'], stats['current_bytes'])
                return statsDto
            finally:
                target_db_engine.dispose()
        else:
            raise DatabaseNotFoundException()
