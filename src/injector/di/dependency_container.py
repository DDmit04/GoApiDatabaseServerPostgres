from injector.config.config_loader_container import config_container
from injector.di.default_dependency_injector import DefaultDependencyInjector
from injector.di.dev_dependency_injector import DevDependencyInjector

is_dev_mode = config_container.get_global_config().get('is_dev_mode')
di_container = DefaultDependencyInjector()
if is_dev_mode:
    di_container = DevDependencyInjector()
