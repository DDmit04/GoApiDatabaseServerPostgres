import os

from injector.config.config_loader import ConfigLoader

config_filepath = os.environ.get("CONFIG_FILEPATH", "config.yaml")

config_container = ConfigLoader(config_filepath)
