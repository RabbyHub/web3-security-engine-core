import os
import logging
import yaml
import re
import json
import itertools
import shutil
from models.rule import Rule, App, DATA_SOURCE, SignType
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
        self.sign_type_list = [SignType.text, SignType.transaction]
        self.data_source_dirname = DATA_SOURCE

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
        rule_list = []
        for sign_type in self.sign_type_list:
            rule_dict = self._walk_dir(os.path.join(REPO_TMP_DIR, app_name, sign_type.name), self._load_rules)            
            for rule in itertools.chain(*rule_dict.values()):
                rule.sign_type = sign_type
                rule_list.append(rule)
        return rule_list

    def _load_rules(self, file):
        with open(file) as f:
            raw_rule_list = yaml.safe_load(f)
            return [Rule(**raw_rule) for raw_rule in raw_rule_list]
            
    def parse_data_source(self, app_name):
        raw_data_source_dict = self._walk_dir(os.path.join(REPO_TMP_DIR, app_name, self.data_source_dirname), self._load_data_source)
        data_source_dict = {filename.split('.')[0]: value for filename, value in raw_data_source_dict.items()}
        return type(DATA_SOURCE, (object,), data_source_dict)
        
    def _load_data_source(self, file):
        suffix = file.split('.')[-1]
        with open(file) as f:
            if suffix == 'json':
                item = json.load(f)
            elif suffix == 'txt':
                item = f.read()
            elif suffix == 'yaml':
                item = yaml.safe_load(f)
        return item

    def parse(self):
        app_list = []
        for app in self.app_list:
            rule_list = self.parse_rule(app['name'])
            data_source = self.parse_data_source(app['name'])
            app = App(name=app['name'], origin=app['origin'], rules=rule_list, data_source=data_source, is_active=True, version=app['version'])
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
                'origin': 'common'
            },
            {
                'url': 'git@github.com:RabbyHub/example-dapp-security-rule.git',
                'branch': 'v0.0.1',
                'origin': 'https://dapp.com'
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
                origin=repo['origin']
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
