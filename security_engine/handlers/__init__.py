
from enum import Enum


class HandlerType(Enum):
    RULE_LOAD = 1
    LOG = 2


class BaseHandler(object):

    @property
    def handler_type(self):
        raise NotImplemented

