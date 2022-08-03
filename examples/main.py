from security_engine.engine import SecurityEngineCore
from examples.custom_runtime.context import get_context
from security_engine.handlers.rule.rule_load_handler import GithubRepoRuleLoadHandler
from security_engine.handlers.log.log_handler import StreamLogHandler
from security_engine.models.action import get_action

def main():
    
    app_list = [
        {
            'url': 'git@github.com:RabbyHub/example-common-security-rule.git', 
            'commit_hash': '999a5b2e175c0e2612b45b0e5abaebfb840eb63e',
            'origin': 'common',
        },
        {
            'url': 'git@github.com:RabbyHub/example-dapp-security-rule.git', 
            'commit_hash': '928e2c8cb41864c81c2c65a69b000c3761c8306c',
            'origin': 'common'
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
