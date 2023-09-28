from contextvars import ContextVar

import constants

ctx = ContextVar(constants.app_context, default=dict())
