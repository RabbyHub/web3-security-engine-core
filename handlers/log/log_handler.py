import logging
from handlers import HandlerType, BaseHandler
from models.rule import ExecuteLog

logger = logging.getLogger('log_handler')

class BaseLogHandler(BaseHandler):

    @property
    def handler_type(self):
        return HandlerType.LOG

    def add_trace_log(self):
        raise NotImplemented

    def output(self):
        raise NotImplemented


class StreamLogHandler(BaseHandler):
    
    def __init__(self) -> None:
        self.trace_log_list = []

    def add_trace_log(self, log):
        self.trace_log_list.append(log)

    def output(self):
        for trace_log in self.trace_list:
            logger.info('text=[{text}] tx=[{tx}] origin=[{origin}] execute rule=[{rule}] at {time_at} hit={hit}'.format(
                text=trace_log.text,
                tx=trace_log.tx,
                origin=trace_log.origin,
                rule=trace_log.rule,
                time_at=trace_log.time_at,
                hit=trace_log.hit
            ))
        self.trace_log_list = []
    