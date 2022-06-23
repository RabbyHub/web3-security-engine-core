# Security Rule Engine Core

Web3 安全规则引擎核心模块


## Rule
> 规则加载和存储
* [Rule](./models/rule.py)
* [GithubRuleLoadHandler](./handlers/rule/rule_load_handler.py)
    

## Log
> 日志收集和处理
* [StreamLogHandler](./handlers/log/log_handler.py)

## Runtime
> 引擎执行的上下文 Context
* [Context](./runtime/context.py)

## Model
> 存储和转换引擎底层 Runtime 对象
* [Tx](./models/transaction.py)
* [Address](./models/address.py)
* [Contract](./models/contract.py)
* [Token](./models/token.py)
* [TokenTranfer](./models/transaction_scene.py)


## Engine
> 规则引擎
* [SecurityEngine](./engine.py)


## Examples

``` python
from engine import SecurityEngine
from examples.custom_runtime.context import CustomContext
from handlers.rule.rule_load_handler import GithubRuleLoadHandler
from handlers.log.log_handler import StreamLogHandler


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

    # Add github rule set handler
    github_repo_url_list = [
        'https://github.com/RabbyHub/example-common-security-rule'
    ]
    rule_load_handler = GithubRuleLoadHandler(github_repo_url_list)
    engine.add_handler(rule_load_handler)

    # Add default log handler
    log_handler = StreamLogHandler()
    engine.add_handler(log_handler)

    # load source to init engine
    engine.load()
    print('load successfuly.')

    for activity in activities:
        context = CustomContext(activity)
        result = engine.run(context)
        for r in result:
            print('description: %s\nlevel: %s' % (r.description, r.level))


if __name__ == '__main__':
    main()

```

## 自定义 RuleLoadHandler

继承 [BaseRuleLoadHandler](./handlers/rule/rule_load_handler.py)

``` Python
class BaseRuleLoadHandler(BaseHandler):
    
    def fetch_raw(self):
        raise NotImplemented
    
    def load(self):
        raise NotImplemented
```

## 自定义 LogHandler

继承 [BaseLogHandler](./handlers/log/log_handler.py)

``` python
class BaseLogHandler(BaseHandler):

    def add_trace_log(self):
        raise NotImplemented

    def output(self):
        raise NotImplemented
```

## 自定义 Context

继承 [Context](./runtime/context.py)
``` python
class Context(BaseContext):
    pass
```




