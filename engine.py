import logging
from readline import insert_text
import time
import inspect
from models.rule import Response
from managers.rule import RuleManager
from managers.log import LogManager
from managers.context import ContextManager
from handlers import BaseHandler, HandlerType


log_manager = LogManager()


class SecurityEngineCore(object):

    def __init__(self, rule_load_handler_list=[]):
        self.rule_manager = RuleManager(load_handlers=rule_load_handler_list)
        
    def load(self, refresh=False):
        self.rule_manager.load(refresh=refresh)
    
    def add_handler(self, handler):
        if handler.handler_type == HandlerType.RULE_LOAD:
            self.rule_manager.add_load_handler(handler)
        elif handler.handler_type == HandlerType.LOG:
            log_manager.add_handler(handler)
        else:
            logging.error('Engine handler type: %s invalid', handler.handler_type)

    def run(self, context):
        self.context_manager = ContextManager(context=context)
        app_list = self.rule_manager.filter(context.origin)
        hit_rules = []
        for app in app_list:
            context = self.context_manager.clone(**dict(data_source=app.data_source))
            rules = self.run_app(context, app)
            hit_rules.extend(rules)
        if hit_rules:
            res = Response(Hit=True, rules=hit_rules)
        else:
            res = Response(Hit=False)
        return res

    @log_manager
    def run_app(self, context, app):
        hit_rules = []
        for rule in app.rules:
            try:
                hit = self.execute(context, rule)
                if not hit:
                    continue
                hit_rules.append(rule)
            except Exception as e:
                logging.error('Eval rule=[%s] error=[%s]', rule.logic, e)
        self.context_manager.add_property(context, 'hit_rules', hit_rules)
        self.context_manager.add_property(context, 'app', app)
        return hit_rules

    def execute(self, context, rule):
        context_dict = self.context_manager.to_dict(context)
        if rule.conditions:
            for condition in rule.conditions:
                rule.logic = rule.logic.replace(condition['condition'], '(%s)' % condition['logic'])
        return eval(rule.logic, context_dict)


    
