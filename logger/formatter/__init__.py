import json
import logging
import os
import traceback
import json_logging
from datetime import datetime

import constants

json_logging.ENABLE_JSON_LOGGING = True


def extra(**kw):
    '''Add the required nested props layer'''
    return {'extra': {'props': kw}}


class CustomJSONLog(logging.Formatter):
    """
    Customized logger
    """
    python_log_prefix = 'python.'

    def __init__(self, message_type='RZPOCRFormatter'):
        self.app_env = os.environ.get('APP_ENV', constants.DEFAULT_ENV_MODE)
        self.message_type = message_type

    def get_exc_fields(self, record):
        if record.exc_info:
            exc_info = self.format_exception(record.exc_info)
        else:
            exc_info = record.exc_text
        return {f'{self.python_log_prefix}exc_info': exc_info}

    @classmethod
    def format_exception(cls, exc_info):
        return ''.join(traceback.format_exception(*exc_info)) if exc_info else ''

    def format(self, record):
        json_log_object = {
            '@timestamp': datetime.utcnow().isoformat(),
            '@message': record.getMessage(),
            '@source_path': record.pathname,
            '@type': self.message_type,
            '@app_env': self.app_env,
            'level': record.levelname,
            'caller': record.filename + '::' + record.funcName,
            '@fields': {
                'logger': record.name,
                'module': record.module,
                'lineno': record.lineno,
                'thread': f'{record.threadName}[{record.thread}]',
                'process': record.process
            },
        }
        if hasattr(record, 'props'):
            json_log_object['@fields'].update(record.props)

        if record.exc_info or record.exc_text:
            json_log_object['@fields'].update(self.get_exc_fields(record))
        # if ctx.get(None) is not None:
        #     json_log_object['@context'] = ctx.get()
        return json.dumps(json_log_object)


def initialize_json_logger():
    json_logging.__init(custom_formatter=CustomJSONLog)
