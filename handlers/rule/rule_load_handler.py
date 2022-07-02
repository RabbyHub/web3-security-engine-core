import os
import logging
import yaml
import re
import itertools
import shutil
from models.rule import Rule, App
from git import Repo
from handlers import HandlerType, BaseHandler


REPO_TMP_DIR = './tmp'

logger = logging.getLogger('rule_load_handler')


class BaseRuleLoadHandler(BaseHandler):
    
    @property
    def handler_type(self):
        return HandlerType.RULE_LOAD

    def fetch_raw(self):
        raise NotImplemented
    
    def load(self):
        raise NotImplemented

        
class FileRuleLoadHandler(BaseRuleLoadHandler):

    def __init__(self, app_list) -> None:
        '''
        app = {
            'name': '',
            'version': ''
        }
        '''
        self.app_list = app_list
        self.transaction_rule_dirname = 'transaction'
        self.data_source_dirname = 'data_source'

    def fetch_raw(self):
        if not os.path.exists(REPO_TMP_DIR):
            os.mkdir(REPO_TMP_DIR)
        return self.app_list

    def _walk_dir(self, dir_path, callback):
        items = {}
        if os.path.exists(dir_path):
            filenames = [filename for filename in os.listdir(dir_path)]
            for filename in filenames:
                objs = callback(os.path.join(dir_path, filename))
                items[filename] = objs
        return items
    
    def parse_rule(self, app_name):
        rule_dict = self._walk_dir(os.path.join(REPO_TMP_DIR, app_name, self.transaction_rule_dirname), self._load_rules)
        rule_list = list(itertools.chain(*rule_dict.values()))
        return rule_list

    def _load_rules(self, file):
        with open(file) as f:
            raw_rule_list = yaml.safe_load(f)
            return [Rule(**raw_rule) for raw_rule in raw_rule_list]
            
    def parse_data_source(self, app_name):
        raw_data_source_dict = self._walk_dir(os.path.join(REPO_TMP_DIR, app_name, self.data_source_dirname), self._load_data_source)
        data_source_dict = {filename.split('.')[0]: value for filename, value in raw_data_source_dict.items()}
        return type('data_source', (object,), data_source_dict)
        
    def _load_data_source(self, file):
        items = []
        with open(file) as f:
            for line in f:
                if line.startswith('#'):
                    continue
                l = line.split('#')[0]
                items.append(l.strip()) if l else None
        return items

    def parse(self):
        app_list = []
        for app in self.app_list:
            rule_list = self.parse_rule(app['name'])
            data_source = self.parse_data_source(app['name'])
            app = App(name=app['name'], domain=app['domain'], rules=rule_list, data_source=data_source, is_active=True, version=app['version'])
            app_list.append(app)
        return app_list

    def load(self):
        return self.parse()


class GithubRepoRuleLoadHandler(FileRuleLoadHandler):

    def __init__(self, repo_list) -> None:
        '''
        repo_list = [
            {
                'url': 'https://github.com/RabbyHub/example-common-security-rule.git',
                'branch': 'main',
                'domain': 'domain'
            },
            {
                'url': 'git@github.com:RabbyHub/example-dapp-security-rule.git',
                'branch': 'v0.0.1',
                'domain': 'dapp.com'
            }
        ]
        '''
        self.repo_list = repo_list
        app_list = self.get_app_list(repo_list)
        super(GithubRepoRuleLoadHandler, self).__init__(app_list)

    @staticmethod
    def get_app_name(repo_url):
        pattern = '(git@github.com:|https:\/\/github.com\/)(?P<filepath>.*)\.git'
        match = re.findall(pattern, repo_url)
        if not match:
            raise Exception('Invalid github repo url:%s' %repo_url)
        return match[0][1].replace('/', '_')

    @classmethod
    def get_app_list(cls, repo_list):
        app_list = []
        for repo in repo_list:
            app_list.append(dict(
                name=cls.get_app_name(repo['url']),
                version=repo['branch'],
                domain=repo['domain']
            ))
        return app_list

    def load(self, refresh=True):
        if refresh:
            self.fetch_raw()
        return self.parse()

    def fetch_raw(self):
        super(GithubRepoRuleLoadHandler, self).fetch_raw()
        assert len(self.repo_list) == len(self.app_list)
        for i, repo in enumerate(self.repo_list):
            local_dst = os.path.join(REPO_TMP_DIR, self.app_list[i]['name'])
            if os.path.exists(local_dst):
                shutil.rmtree(local_dst)
            Repo.clone_from(repo['url'], local_dst, multi_options=['-b %s' % repo['branch']])
