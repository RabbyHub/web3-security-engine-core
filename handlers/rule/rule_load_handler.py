import os
import logging
import yaml
import re
import json
import itertools
import shutil
from models.rule import Rule, App, DATA_SOURCE, SignType
from git import Object, Repo
from handlers import HandlerType, BaseHandler


REPO_TMP_DIR = './tmp'
RULE_SET_DIR = 'ruleset'
ADDRESS_SET_DIR = 'address_set'
DOMAIN_SET_DIR = 'domain_set'
SIGN_TEXT_PATTERN_SET_DIR = 'sign_text_pattern_set'

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
        self.app_list = app_list
        self.sign_type_list = [SignType.text, SignType.transaction]
        self.data_source_dir_list = [ADDRESS_SET_DIR, DOMAIN_SET_DIR, SIGN_TEXT_PATTERN_SET_DIR]

    def fetch_raw(self):
        if not os.path.exists(REPO_TMP_DIR):
            os.mkdir(REPO_TMP_DIR)
        return self.app_list

    def _walk_dir(self, dir_path, callback):
        item = {}
        if os.path.exists(dir_path):
            filenames = [filename for filename in os.listdir(dir_path)]
            for filename in filenames:
                sub_dir_path = os.path.join(dir_path, filename)
                if os.path.isdir(sub_dir_path):
                    objs = self._walk_dir(sub_dir_path, callback)
                else:
                    objs = callback(os.path.join(dir_path, filename))
                item[filename.split('.')[0]] = objs
        return item
    
    def parse_rule(self, app_name):
        rule_list = []
        for sign_type in self.sign_type_list:
            rule_dict = self._walk_dir(os.path.join(REPO_TMP_DIR, app_name, RULE_SET_DIR, sign_type.name), self._load_rules)            
            for rule in itertools.chain(*rule_dict.values()):
                rule.sign_type = sign_type
                rule_list.append(rule)
        return rule_list

    def _load_rules(self, file):
        with open(file) as f:
            raw_rule_list = yaml.safe_load(f)
            return [Rule(**raw_rule) for raw_rule in raw_rule_list]
            
    def parse_data_source(self, app_name):
        data_source_dict = {}
        for data_source_dirname in self.data_source_dir_list:
            raw_data_source_dict = self._walk_dir(os.path.join(REPO_TMP_DIR, app_name, data_source_dirname), self._load_data_source)
            data_source_dict.update({
                data_source_dirname: type(data_source_dirname, (object,), raw_data_source_dict)
            })
            # import pdb;pdb.set_trace()
            # for k, v in raw_data_source_dict.items():
            #     import pdb;pdb.set_trace()
                
            #     data_source_dict.update({
            #         k: v
            #     })
        return data_source_dict
        
    def _load_data_source(self, file):
        suffix = file.split('.')[-1]
        item = None
        with open(file) as f:
            if suffix == 'json':
                item = json.load(f)
            elif suffix == 'txt':
                if SIGN_TEXT_PATTERN_SET_DIR in file:
                    item = f.read()
                else:
                    item = []
                    for line in f:
                        if line.startswith('#'):
                            continue
                        l = line.split('#')[0]
                        item.append(l.strip()) if l else None
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
        self.repo_list = repo_list
        app_list = self.get_app_list(repo_list)
        super(GithubRepoRuleLoadHandler, self).__init__(app_list)

    @staticmethod
    def get_app_name(repo_url):
        pattern = '(git@github.com:|https:\/\/github.com\/)(?P<filepath>.*)'
        match = re.findall(pattern, repo_url)
        if not match:
            raise Exception('Invalid github repo url:%s' %repo_url)
        if not repo_url.endswith('.git'):
            repo_url += '.git'
        return match[0][1].replace('/', '_')

    @classmethod
    def get_app_list(cls, repo_list):
        app_list = []
        for repo in repo_list:
            app_list.append(dict(
                name=cls.get_app_name(repo['url']),
                version=repo['commit_hash'],
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
            repo_object = Repo.clone_from(repo['url'], local_dst)
            # import pdb;pdb.set_trace()
            repo_object.head.reset(commit=repo['commit_hash'])
