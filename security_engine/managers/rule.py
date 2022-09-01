from security_engine.models.rule import COMMON_ORIGIN
from security_engine.models.data_source import DataSource


class RuleManager(object):

    def __init__(self, load_handlers=[]) -> None:
        self.load_handlers = load_handlers
        self.app_list = []

    def load(self, refresh=True):
        app_list = []
        for load_handler in self.load_handlers:
            app_list.extend(load_handler.load(refresh=refresh))
        self.app_list = app_list
        
    def add_load_handler(self, handler):
        self.load_handlers.append(handler)
    
    def get_data_source_dict(self, app):
        data_source_dict = {}
        for set_name, source_dict in app.data_source.items():
            source = {}
            for k, v in source_dict.items():
                if callable(v):
                    source[k] = v()
                else:
                    source[k] = v
            data_source_dict[set_name] = DataSource.from_dict(source)
        return data_source_dict

    def filter(self, origin=''):
        rule_app_list = []
        for app in self.app_list:
            if app.origin == COMMON_ORIGIN:
                rule_app_list.append(app)
            elif app.origin == origin:
                rule_app_list.append(app)
        return rule_app_list
                


