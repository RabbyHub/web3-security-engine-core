# Security Rule Engine Core

Web3 安全规则引擎核心模块

![](./process.jpg)

## Rule

> 规则加载和存储

- [App](./models/rule.py)
- [Rule](./models/rule.py)
- [GithubRuleLoadHandler](./handlers/rule/rule_load_handler.py)

## Log

> 日志收集和处理

- [StreamLogHandler](./handlers/log/log_handler.py)

## Runtime

> 引擎执行的上下文 Context

- [Context](./runtime/context.py)

## Manager

> 负责管理 engine 中的 Handler & Runtime

- [RuleManager](./managers/rule.py)
- [LogManager](./managers/log.py)
- [ContextManager](./managers/context.py)

## Model

> 存储和转换引擎底层 Runtime 对象

- [Tx](./models/transaction.py)
- [Address](./models/address.py)
- [Contract](./models/contract.py)
- [Token](./models/token.py)
- [TokenTranfer](./models/transaction_scene.py)

## Engine

> 规则引擎

- [SecurityEngine](./engine.py)

## Examples

```python
from engine import SecurityEngineCore
from examples.custom_runtime.context import get_context
from handlers.rule.rule_load_handler import GithubRepoRuleLoadHandler
from handlers.log.log_handler import StreamLogHandler
from models.action import get_action

def main():

    app_list = [
        {
            'url': 'git@github.com:RabbyHub/example-common-security-rule.git',
            'branch': 'master',
            'origin': 'common',
        },
        {
            'url': 'git@github.com:RabbyHub/example-dapp-security-rule.git',
            'branch': 'master',
            'origin': 'https://dapp.com'
        },
        {
            'url': 'git@github.com:DeBankDeFi/dapp-security-rules.git',
            'branch': 'main',
            'origin': 'https://debank.com'
        }

    ]

    engine = SecurityEngineCore()
    rule_load_handler = GithubRepoRuleLoadHandler(app_list)
    engine.add_handler(rule_load_handler)

    # Add default log handler
    log_handler = StreamLogHandler()
    engine.add_handler(log_handler)

    engine.load()
    print('load successfuly.')


    params = [
        {
            "transaction": {
                "chainId": 42161,
                "data": "0x",
                "from": "0x34799a3314758b976527f8489e522e835ed8d0d2",
                "gas": "0x5208",
                "gasPrice": "0x1dcd65000",
                "nonce": "0x0",
                "to": "0x5853ed4f26a3fcea565b3fbc698bb19cdf6deb85",
                "value": "0x5efe7ec8b12d9c8"
            },
            "origin": "https://debank.com/"
        },
        {
            "text": '''Please sign to let us verify that you are the owner of this address 0x133ad1b948badb72ea0cfbb5a724b5b77c9b6311.
[2022-07-20 06:15:02]''',
            "chain_id": 1,
            "origin": "https://debank.com/"
        },
        {
            "text": '''Spam text signature''',
            "chain_id": 1,
            "origin": "https://debank.com/"
        }
    ]

    for param in params:
        action = get_action(param)
        if not action:
            print('invalid param')
            return
        context = get_context(action)
        result = engine.run(context)

        print('hits=%s' % result.hits)
        print('.................')

if __name__ == '__main__':
    main()


```

## 自定义 RuleLoadHandler

继承 [BaseRuleLoadHandler](./handlers/rule/rule_load_handler.py)

```Python
class BaseRuleLoadHandler(BaseHandler):

    def fetch_raw(self):
        raise NotImplemented

    def load(self):
        raise NotImplemented
```

## 自定义 LogHandler

继承 [BaseLogHandler](./handlers/log/log_handler.py)

```python
class BaseLogHandler(BaseHandler):

    def add_trace_log(self):
        raise NotImplemented

    def output(self):
        raise NotImplemented
```

## 自定义 Context

继承 [Context](./runtime/context.py)

```python
class Context(BaseContext):
    pass
```
