
from logger import get_logger
from context import Context
from models.rule import RuleResult
from mixin.rule import DefaultRuleLoadMixin

logger = get_logger('engine')


class BaseEngine(object):
    
    def __init__(self):
        self.rules = []
        self.source = None

    def eval_rule(self, rule):
        raise NotImplementedError
    
    def initalize(self):
        raise NotImplementedError
        
    def check(self, activity):
        raise NotImplementedError


class SecurityEngine(BaseEngine, DefaultRuleLoadMixin):

    def __init__(self):
        super().__init__()

    def initalize(self):
        self.load_rules()
        self.load_sources()

    def eval_rule(self, context, rule):
        try:
            return eval(rule.logic, context)
        except Exception as e:
            logger.error('Eval rule=[%s] error=[%s]', rule.logic, e)
    
    def init_context(self, activity):
        context = Context(activity, self.source)
        return context

    def check(self, activity):
        context = self.init_context(activity)
        result = []
        for rule in self.rules:
            res = self.eval_rule(context.local_ctx, rule)
            if not res:
                continue
            result.append(
                RuleResult(description=rule.description, 
                level=rule.level)
                )
        return result


def main():
    
    activities = [
        {
            'transaction': {
                "chainId": 42161, 
                "data": "0x", 
                "from": "0x34799a3314758b976527f8489e522e835ed8d0d2", 
                "gas": "0x5208", 
                "gasPrice": "0x1dcd65000", 
                "nonce": "0x0", 
                "to": "0x81Fbf7d00316610Bae86Ae52F40908fF571F670A", 
                "value": "0x5efe7ec8b12d9c8"
            },
            'text': None,
            'origin': "https://quickswap.exchange"
        }
    ]

    engine = SecurityEngine()
    engine.initalize()
    print('initalized successfuly.')

    for activity in activities:
        result = engine.check(activity)
        for r in result:
            print('description: %s\nlevel: %s' % (r.description, r.level))


if __name__ == '__main__':
    main()

    
