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
