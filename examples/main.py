from engine import SecurityEngineCore
from examples.custom_runtime.context import CustomContext
from handlers.rule.rule_load_handler import GithubRepoRuleLoadHandler
from handlers.log.log_handler import StreamLogHandler


def main():
    
    action = {
            'transaction': {
                "chainId": 42161, 
                "data": "0x", 
                "from": "0x34799a3314758b976527f8489e522e835ed8d0d2", 
                "gas": "0x5208", 
                "gasPrice": "0x1dcd65000", 
                "nonce": "0x0", 
                "to": "0x5853ed4f26a3fcea565b3fbc698bb19cdf6deb85", 
                "value": "0x5efe7ec8b12d9c8"
            },
            'text': None,
            'origin': "https://quickswap.exchange"
        }

    engine = SecurityEngineCore()

    app_list = [
        {
            'url': 'git@github.com:RabbyHub/example-common-security-rule.git', 
            'branch': 'master',
            'domain': 'common',
        },
        {
            'url': 'git@github.com:RabbyHub/example-dapp-security-rule.git', 
            'branch': 'master',
            'domain': 'app.uniswap.org'
        }
    ]

    rule_load_handler = GithubRepoRuleLoadHandler(app_list)
    engine.add_handler(rule_load_handler)

    # Add default log handler
    log_handler = StreamLogHandler()
    engine.add_handler(log_handler)

    engine.load()
    print('load successfuly.')

    context = CustomContext(action)
    result = engine.run(context)

    print('hit=%s, rules=%s' % (result.Hit, result.rules))


if __name__ == '__main__':
    main()
