import logging
import sys

from logger import formatter as log_formatter


class LogProvider(object):
    """
    Class to provide Log Handlers
    """
    _instance = None

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance

    def __init__(self, root_logger=True, logger_name="local"):
        log_formatter.initialize_json_logger()
        if root_logger:
            self.logger = logging.RootLogger(logging.INFO)
        else:
            self.logger = logging.Logger(logger_name)

        handler = self.get_stdout_handler(root_logger)

        # The below is needed so that logs
        # do not appear multiple times
        # Reference: https://stackoverflow.com/questions/6729268/python-logging-messages-appearing-twice
        if not self.logger.handlers:
            self.logger.addHandler(handler)

    @classmethod
    def get_logger(cls):
        """
            Method to provide configs
        """
        instance = cls.get_instance()

        return instance.logger

    @classmethod
    def get_stdout_handler(cls, root_logger):
        # Directing output to stdout
        handler = logging.StreamHandler(sys.stdout)
        if root_logger:
            handler.setLevel(logging.INFO)
        return handler
