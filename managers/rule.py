from git import refresh


class RuleManager(object):

    def __init__(self, load_handlers=[]) -> None:
        self.load_handlers = load_handlers
        self.app_list = []

    def load(self, refresh=True):
        for load_handler in self.load_handlers:
            self.app_list.extend(load_handler.load(refresh=refresh))
        
    def add_load_handler(self, handler):
        self.load_handlers.append(handler)
    
    def filter(self, origin=''):
        rule_app_list = []
        for app in self.app_list:
            if app.domain == 'common':
                rule_app_list.append(app)
            elif app.domain in origin:
                rule_app_list.append(app)
        return rule_app_list
                


