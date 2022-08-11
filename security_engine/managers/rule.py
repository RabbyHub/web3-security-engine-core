from security_engine.models.rule import COMMON_ORIGIN
from security_engine.models.data_source import DataSource


class RuleManager(object):

    def __init__(self, load_handlers=[]) -> None:
        self.load_handlers = load_handlers
        self.app_list = []

    def load(self, refresh=True):
        for load_handler in self.load_handlers:
            self.app_list.extend(load_handler.load(refresh=refresh))
        
    def add_load_handler(self, handler):
        self.load_handlers.append(handler)
    
    def validate():
        # todo sandbox validate
        pass
    
    def get_data_source_dict(self, app):
        data_source_dict = {}
        for k, v in app.data_source.items():
            data_source_dict[k] = DataSource.from_dict(v)
        return data_source_dict

    def filter(self, origin=''):
        rule_app_list = []
        for app in self.app_list:
            if app.origin == COMMON_ORIGIN:
                rule_app_list.append(app)
            elif app.origin == origin:
                rule_app_list.append(app)
        return rule_app_list
                


