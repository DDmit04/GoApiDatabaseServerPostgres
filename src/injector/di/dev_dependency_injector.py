from unittest.mock import Mock

from injector.di.default_dependency_injector import DefaultDependencyInjector
from model.databse_service_tables import local_database_model
from service.server.server_database_service import ServerDatabaseService
from service.server.server_register_service import ServerRegisterService


class DevDependencyInjector(DefaultDependencyInjector):

    def get_server_register_service(self, session_id):
        app_database_service = self.get_app_database_service(session_id)
        server_register_service_mock = Mock(spec=ServerRegisterService)
        return server_register_service_mock

    def get_database_service(self):
        return ServerDatabaseService(local_database_model)
