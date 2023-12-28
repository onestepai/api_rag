import logging
from ServiceOneStepCore.Utilities.MyEnvironment import MyEnvironment


class LoggerHelper(object):

    # log level
    LEVEL_CRITICAL = 'critical'
    LEVEL_WARNING = 'warning'
    LEVEL_INFO = 'info'
    LEVEL_NOTSET = 'notset'

    # log level value
    CRITICAL_VALUE = 50
    ERROR_VALUE = 40
    WARNING_VALUE = 30
    INFO_VALUE = 20
    DEBUG_VALUE = 10
    NOTSET_VALUE = 0

    def __init__(self):
        self._log_level = MyEnvironment().get_log_level()
        self._set_log_level()
        pass

    def _set_log_level(self):
        # root logger
        root = logging.getLogger()
        root.setLevel(logging.INFO)
        if self._log_level == self.LEVEL_CRITICAL:
            self._log_level_value = self.CRITICAL_VALUE
            #root.setLevel(logging.CRITICAL)
        elif self._log_level == self.LEVEL_WARNING:
            self._log_level_value = self.WARNING_VALUE
            #root.setLevel(logging.WARNING)
        elif self._log_level == self.LEVEL_INFO:
            self._log_level_value = self.INFO_VALUE
            #root.setLevel(logging.INFO)
        else:
            self._log_level_value = self.NOTSET_VALUE
            #root.setLevel(logging.NOTSET)

    def _is_enabled_for(self, level):
        return level >= self._log_level_value

    def log_critical(self, msg):
        logging.critical(msg)

    def log_warning(self, msg):
        logging.warning(msg)


    def log_info(self, msg):
        logging.info(msg)
