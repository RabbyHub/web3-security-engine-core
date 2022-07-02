import logging
import time
from handlers import HandlerType, BaseHandler
from models.rule import ExecuteLog
from runtime.context import Context


class BaseLogHandler(BaseHandler):

    @property
    def handler_type(self):
        return HandlerType.LOG

    def output(self):
        raise NotImplemented


class StreamLogHandler(BaseLogHandler):
    
    def __init__(self) -> None:
        super(StreamLogHandler, self).__init__()
        
    def output(self, context: Context):    
        log = ExecuteLog(origin=context.origin, text=context.text, 
                   tx=context.tx, app=context.app, 
                   hit_rules=context.hit_rules,
                   time_at=time.time()
                   )
        print('log entry:', log)