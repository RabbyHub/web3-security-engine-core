import logging
import pprint
import time
from security_engine.handlers import HandlerType, BaseHandler
from security_engine.models.rule import App, ExecuteLog
from security_engine.runtime.context import BaseContext


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
                   app=app,
                   hit_rules=context.hit_rules,
                   action=context.action, 
                   time_at=time.time()
                   )
        if hasattr(context, 'error'):
            log.error = context.error
        pprint.pprint(log)
        print('\n')