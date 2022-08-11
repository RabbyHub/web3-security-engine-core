import dataclasses
from enum import Enum
from typing import List, Dict
from .action import BaseAction, SignType

COMMON_ORIGIN = 'common'
DATA_SOURCE = 'data_source'


class Level(Enum):
    Safe = 0
    Warning = 1
    Danger = 2
    Forbidden = 3


@dataclasses.dataclass()
class Condition(object):
    condition: str
    description: str
    logic: str


@dataclasses.dataclass()
class Rule(object):
    description: str
    level: Level
    logic: str
    sign_type: SignType = dataclasses.field(init=False)
    conditions: List[Condition] = dataclasses.field(default_factory=list)
    properties: Dict = dataclasses.field(default_factory=dict)


@dataclasses.dataclass()
class App(object):
    name: str
    rules: List[Rule]
    data_source: Dict
    is_active: bool
    version: str
    origin: str = COMMON_ORIGIN


@dataclasses.dataclass()
class Hit(object):
    app: App
    level: str
    rules: List[Rule] = dataclasses.field(default_factory=list)
    

@dataclasses.dataclass()
class Response(object):
    hits: List[Hit] = dataclasses.field(default_factory=list)


@dataclasses.dataclass()
class ExecuteLog(object):
    app: App
    action: BaseAction
    time_at: int
    hit_rules: List[Rule]
    error: str = None

