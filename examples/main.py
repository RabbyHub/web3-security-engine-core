from security_engine.engine import SecurityEngineCore
from examples.custom_runtime.context import get_context
from security_engine.handlers.rule.rule_load_handler import GithubRepoRuleLoadHandler
from security_engine.handlers.log.log_handler import StreamLogHandler
from security_engine.models.action import get_action

def main():
    
    repo_list = [
            {
                'url': 'https://github.com/RabbyHub/web3-security-rules',
                'commit_hash': 'a72d4c8b669bf8493d772f5b4097e82db85c4318',
                'origin': 'common',
            },
            {
                'url': 'https://github.com/RabbyHub/example-dapp-security-rule',
                'commit_hash': '928e2c8cb41864c81c2c65a69b000c3761c8306c',
                'origin': 'http://debank.com',
            },
            {
                'url': 'https://github.com/RabbyHub/example-common-security-rule',
                'commit_hash': '73cad96c6f08294e0fd907f0f225c175e9a1c6b5',
                'origin': 'common',
            },
        ]
    
    engine = SecurityEngineCore()
    rule_load_handler = GithubRepoRuleLoadHandler(repo_list, 'demo token')
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
        },
        {
            "typed_data": {
                "types": {
                    "EIP712Domain": [
                    {
                        "name": "name",
                        "type": "string"
                    },
                    {
                        "name": "version",
                        "type": "string"
                    },
                    {
                        "name": "chainId",
                        "type": "uint256"
                    },
                    {
                        "name": "verifyingContract",
                        "type": "address"
                    }
                    ],
                    "Permit": [
                    {
                        "name": "owner",
                        "type": "address"
                    },
                    {
                        "name": "spender",
                        "type": "address"
                    },
                    {
                        "name": "value",
                        "type": "uint256"
                    },
                    {
                        "name": "nonce",
                        "type": "uint256"
                    },
                    {
                        "name": "deadline",
                        "type": "uint256"
                    }
                    ]
                },
                "domain": {
                    "name": "USD Coin",
                    "version": "2",
                    "verifyingContract": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
                    "chainId": 1
                },
                "primaryType": "Permit",
                "message": {
                    "owner": "0x5853eD4f26A3fceA565b3FBC698bb19cdF6DEB85",
                    "spender": "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45",
                    "value": "1000000",
                    "nonce": 7,
                    "deadline": 1658834549
                }
                },
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
