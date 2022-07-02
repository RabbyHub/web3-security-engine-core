import dataclasses
from typing import Optional
from .transaction import Tx


@dataclasses.dataclass()
class Condition(object):
    condition: str
    description: str
    logic: str


@dataclasses.dataclass()
class Rule(object):
    description: str
    level: str
    logic: str
    conditions: list[Condition] = dataclasses.field(default_factory=list)


@dataclasses.dataclass()
class App(object):
    name: str
    rules: list[Rule]
    data_source: object
    is_active: bool
    version: str
    domain: str = 'common'
    

@dataclasses.dataclass()
class Response(object):
    Hit: bool
    rules: list[Rule] = dataclasses.field(default_factory=list)


@dataclasses.dataclass()
class ExecuteLog(object):
    origin: str
    text: str
    tx: Tx
    app: App
    hit_rules: list[Rule]
    time_at: int
    

