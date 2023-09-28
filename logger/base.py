from logger.handler import LogProvider


class BaseLogger(object):
    """
    Base class for logger.
    """

    def __init__(self):
        self._use_local_logger = False
        self._local_logger = None
        self._logger_name = "local"

    @property
    def logger(self):
        """
            Method to provide log handler
        """
        if self._use_local_logger:
            return self.get_local_logger()
        else:
            return LogProvider.get_logger()

    def use_local_logger(self, should_use, logger_name="local"):
        """
        :param should_use: Set to true to use local log instance
        and false to use global singleton
        :param logger_name: Logger name
        """
        self._use_local_logger = should_use
        self._logger_name = logger_name

    def get_local_logger(self):
        """
        :return: Local logger instance where log level is not overridden
        """
        if not self._local_logger:
            provider = LogProvider(root_logger=False, logger_name=self._logger_name)
            self._local_logger = provider.logger
        return self._local_logger
