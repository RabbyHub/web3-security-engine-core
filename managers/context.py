import copy

class ContextManager(object):
    
    def __init__(self, context) -> None:
        self.context = context

    @staticmethod
    def add_property(context, key, value):
        setattr(context, key, value)
    
    def clone(self, **kwargs):
        context = copy.deepcopy(self.context)
        for k, v in kwargs.items():
            self.add_property(context, k, v)
        return context
    
    def to_dict(self, context):
        attr_dict = dict()
        for attr in dir(context):
            if not attr.startswith('__'):
                attr_dict[attr] = getattr(context, attr)
        return attr_dict