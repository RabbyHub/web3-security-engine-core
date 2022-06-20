import os
import yaml
from dataclasses import make_dataclass
from models.rule import Rule

BASE_DIR = '../example-common-security-rule'


class DefaultRuleLoadMixin(object):

    def __init__(self, base_dir) -> None:
        self.transaction_rule_dir = os.path.join(base_dir, 'transaction')
        self.source_dir = os.path.join(base_dir, 'source')

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
    
    def load_rules(self):
        raw_rule_list = self._walk_dir(self.transaction_rule_dir, self.parse_rule)
        self.rules.append([Rule(**raw_rule[1]) for raw_rule in raw_rule_list])

    def parse_rule(self, file):
        with open(file) as f:
            rule_dict = yaml.safe_load(f)
            return rule_dict

    def load_sources(self):
        attrs_tuble_list = self._walk_dir(self.source_dir, self.parse_source)
        attr_value_dict = {i[0].split('.')[0]: i[1] for i in attrs_tuble_list}
        Source = make_dataclass('Source', attr_value_dict.keys(), bases=(object,))
        self.source = Source(**attr_value_dict.values())

    def parse_source(self, file):
        objs = []
        with open(file) as f:
            for line in f:
                if line.startswith('#'):
                    continue
                l = line.split('#')[0]
                objs.append(l) if l else None
        return objs
