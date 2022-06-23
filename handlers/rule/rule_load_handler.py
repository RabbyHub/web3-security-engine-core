import os
import yaml
from dataclasses import make_dataclass
from models.rule import Rule
from handlers import HandlerType, BaseHandler


class BaseRuleLoadHandler(BaseHandler):
    
    @property
    def handler_type(self):
        return HandlerType.RULE_LOAD

    def fetch_raw(self):
        raise NotImplemented
    
    def load(self):
        raise NotImplemented

        
class FileRuleLoadHandler(BaseRuleLoadHandler):

    def __init__(self, filepath_list) -> None:
        self.filepath_list = filepath_list
        self.transaction_rule_dirname = 'transaction'
        self.data_source_dirname = 'data_source'

    def fetch_raw(self):
        return self.filepath_list

    def _walk_dir(self, dir_path, callback):
        objs = []
        if os.path.exists(dir_path):
            files = [filename for filename in os.listdir(dir_path)]
            for filename in files:
                obj, err = callback(os.path.join(dir, filename))
                if err:
                    print(err)
                else:
                    objs.append((filename, obj))
        return objs
    
    def parse_rule(self):
        rule_list = []
        for filepath in self.filepath_list:
            raw_rule_list = self._walk_dir(os.path.join(filepath, self.transaction_rule_dirname), self._load_rule)
            rule_list.append([Rule(**raw_rule[1]) for raw_rule in raw_rule_list])
        return rule_list

    def _load_rule(self, file):
        with open(file) as f:
            rule_dict = yaml.safe_load(f)
            return rule_dict

    def parse_data_source(self):
        data_sources = []
        for filepath in self.filepath_list:
            attrs_tuble_list = self._walk_dir(os.path.join(filepath, self.data_source_dirname), self._load_data_source)
            attr_value_dict = {i[0].split('.')[0]: i[1] for i in attrs_tuble_list}
            DataSource = make_dataclass('DataSource', attr_value_dict.keys(), bases=(object,))
            data_sources.append(DataSource(**attr_value_dict.values()))
        return data_sources

    def _load_data_source(self, file):
        objs = []
        with open(file) as f:
            for line in f:
                if line.startswith('#'):
                    continue
                l = line.split('#')[0]
                objs.append(l) if l else None
        return objs

    def parse(self):
        rule_list = self.parse_rule()
        data_source_list = self.parse_data_source()
        return rule_list, data_source_list

    def load(self):
        self.fetch_raw()
        return self.parse()


class GithubRuleLoadHandler(FileRuleLoadHandler):

    def __init__(self, github_repo_url_list) -> None:
        self.github_repo_url_list = github_repo_url_list
        super().__init__(github_repo_url_list)

    def load(self):
        return super().load()

    def fetch_raw(self):
        # todo git clone reop
        return super().fetch()

    def parse(self):
        return super().parse()