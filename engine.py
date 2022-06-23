import logging
import time
from models.rule import RuleHit, ExecuteLog
from handlers import BaseHandler, HandlerType

logger = logging.getLogger('engine')


class SecurityEngine(object):

    def __init__(self, rule_load_handler_list=[], log_handler_list=[]):
        self.handler_map = {
            HandlerType.RULE_LOAD: rule_load_handler_list,
            HandlerType.LOG: log_handler_list,
        }
        self.rule_list = []
        self.data_source_list = []
    
    def load(self):
        for handler_type, handler_list in self.handler_map:
            logger.info('Load handler type=[%s], handler_list=[%s]', handler_type, handler_list)
            if handler_type == HandlerType.RULE_LOAD:
                for handler in handler_list:
                    rule_list, data_source_list = handler.load()
                    self.rule_list.extend(rule_list)
                    self.data_source_list.extend(data_source_list)
            elif handler_type == HandlerType.LOG:
                pass
    
    def add_handler(self, handler: BaseHandler):
        if handler.handler_type not in self.handler_map:
            logger.error('Handler type: %s invalid', handler.handler_type)
        self.handler_map[handler.handler_type].append(handler)

    def pre_hook(self, context):
        # hook data source
        if self.data_source_list:
            # todo data source is dict, need unique namespace 
            context.add_property('data_source', self.data_source_list)
        return context

    def trace_log(self, context, rule, err, hit):
        log_handler_list = self.handler_map[HandlerType.LOG]
        log = ExecuteLog(origin=context.origin, text=context.text, tx=context.tx, 
                   rule=rule, err=err, hit=hit, time_at=time.time())
        for handler in log_handler_list:
            handler.add_trace_log(log)
        
    def post_hook(self):
        log_handler_list = self.handler_map[HandlerType.LOG]
        for handler in log_handler_list:
            handler.output()

    def run(self, context):
        context = self.pre_hook(context)
        hit_list = []
        for rule in self.rules:
            hit, err = self.execute(context, rule)
            self.trace_log(context, rule, err, hit)
            if not hit:
                continue
            hit_list.append(RuleHit(description=rule.description,  level=rule.level))
        self.post_hook()
        return hit_list

    def execute(self, context, rule):
        try:
            if rule.conditions:
                for c in rule.conditions:
                    rule.logic.replace(c.condition, '(%s)' % c.logic)
            return eval(rule.logic, context), None
        except Exception as e:
            logger.error('Eval rule=[%s] error=[%s]', rule.logic, e)
            return None, str(e)
    



    
