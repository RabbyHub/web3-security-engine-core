import os
import logging
import yaml
import io
import zipfile
import re
import json
import requests
import itertools
import shutil
from security_engine.models.rule import Rule, App, SignType
from security_engine.models.data_source import AddressSet, DomainSet, SignTextPatternSet
from security_engine.handlers import HandlerType, BaseHandler


REPO_TMP_DIR = 'tmp'
RULE_SET_DIR = 'ruleset'


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
        self.sign_type_list = [SignType.text, SignType.typed_data, SignType.transaction]
        self.data_source_class_list = [AddressSet, DomainSet, SignTextPatternSet]

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
                rule.sign_type = sign_type.value
                rule_list.append(rule)
        return rule_list

    def _load_rules(self, file):
        with open(file) as f:
            raw_rule_list = yaml.safe_load(f)
            return [Rule(**raw_rule) for raw_rule in raw_rule_list]
            
    def parse_data_source(self, app_name):
        data_source_dict = {}
        for data_source_class in self.data_source_class_list:
            raw_data_source_dict = self._walk_dir(os.path.join(REPO_TMP_DIR, app_name, data_source_class.__name__), self._load_data_source)
            data_source_dict.update({data_source_class.__name__: raw_data_source_dict})
        return data_source_dict
        
    def _load_data_source(self, file):
        suffix = file.split('.')[-1]
        item = None
        with open(file) as f:
            if suffix == 'json':
                item = json.load(f)
            elif suffix == 'txt':
                if SignTextPatternSet.__name__ in file:
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

    def __init__(self, repo_list, auth_token) -> None:
        self.headers = {'Accept': 'application/vnd.github+json', 'Authorization': auth_token }
        self.repo_list = repo_list
        app_list = self.get_app_list(repo_list)
        super(GithubRepoRuleLoadHandler, self).__init__(app_list)

    @staticmethod
    def get_app_name(repo_url):
        pattern = '(https:\/\/github.com\/)(?P<filepath>.*)'
        match = re.findall(pattern, repo_url)
        if not match:
            raise Exception('Invalid github repo url:%s' % repo_url)
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
            self.download_repo_file(repo, local_dst)

    def download_repo_file(self, repo, local_dst):
        if os.path.exists(local_dst):
            shutil.rmtree(local_dst)
        *_, owner, repo_name = repo['url'].split('/')
        gen_download_url = "https://api.github.com/repos/{owner}/{repo_name}/zipball/{commit_hash}".format(owner=owner, repo_name=repo_name, commit_hash=repo['commit_hash'])
        archive_url = requests.get(gen_download_url, headers=self.headers).url
        r = requests.get(archive_url)

        zip_ref = zipfile.ZipFile(io.BytesIO(r.content))
        zip_ref.extractall(REPO_TMP_DIR)
        os.rename(os.path.join(REPO_TMP_DIR, zip_ref.namelist()[0]), local_dst)