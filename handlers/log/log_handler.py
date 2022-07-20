import logging
import time
from handlers import HandlerType, BaseHandler
from models.rule import App, ExecuteLog
from runtime.context import BaseContext


class BaseLogHandler(BaseHandler):

    @property
    def handler_type(self):
        return HandlerType.LOG

    def output(self):
        raise NotImplemented


class StreamLogHandler(BaseLogHandler):
    
    def __init__(self) -> None:
        super(StreamLogHandler, self).__init__()
        
    def output(self, context: BaseContext):
        app = App(name=context.app.name, 
                is_active=context.app.is_active, 
                version=context.app.version, 
                origin=context.app.origin,
                data_source=None,
                rules=None
                )

        log = ExecuteLog(
                   action=context.action, app=app, 
                   hit_rules=context.hit_rules,
                   time_at=time.time()
                   )
        if hasattr(context, 'error'):
            log.error = context.error
        print('log entry:', log)