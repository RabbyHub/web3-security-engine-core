import logging
from models.rule import Hit, Response, Level, App
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
        hits = []
        for app in app_list:
            context = self.context_manager.clone(**app.data_source)
            hit_rules, level = self.run_app(context, app)
            if hit_rules:
                simple_app = App(name=app.name, 
                    is_active=app.is_active, 
                    version=app.version, 
                    origin=app.origin,
                    data_source=None,
                    rules=None
                )
                hit = Hit(app=simple_app, rules=hit_rules, level=level)
                hits.append(hit)
        res = Response(hits=hits)
        return res

    @log_manager
    def run_app(self, context, app):
        hit_rules = []
        level = Level.Safe.value
        for rule in app.rules:
            if rule.sign_type != context.sign_type:
                continue
            try:
                hit = self.execute(context, rule)
                if not hit:
                    continue
                if rule.level > level:
                    level = rule.level
                hit_rules.append(rule)
            except Exception as e:
                self.context_manager.add_property(context, 'error', e)
                logging.exception('Eval rule=[%s] error=[%s]', rule.logic, e)
        self.context_manager.add_property(context, 'hit_rules', hit_rules)
        self.context_manager.add_property(context, 'app', app)
        return hit_rules, level

    def execute(self, context, rule):
        context_dict = self.context_manager.to_dict(context)
        if rule.properties:
            properties = {k: eval(v, context_dict) for k, v in rule.properties.items()}
            context_dict.update(properties)
        if rule.conditions:
            for condition in rule.conditions:
                rule.logic = rule.logic.replace(condition['condition'], '(%s)' % condition['logic'])
        return eval(rule.logic, context_dict)


    
