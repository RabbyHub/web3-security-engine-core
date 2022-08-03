import dataclasses
from enum import Enum
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
    conditions: list[Condition] = dataclasses.field(default_factory=list)
    properties: dict = dataclasses.field(default_factory=dict)


@dataclasses.dataclass()
class App(object):
    name: str
    rules: list[Rule]
    data_source: dict
    is_active: bool
    version: str
    origin: str = COMMON_ORIGIN


@dataclasses.dataclass()
class Hit(object):
    app: App
    level: str
    rules: list[Rule] = dataclasses.field(default_factory=list)
    

@dataclasses.dataclass()
class Response(object):
    hits: list[Hit] = dataclasses.field(default_factory=list)


@dataclasses.dataclass()
class ExecuteLog(object):
    app: App
    action: BaseAction
    time_at: int
    hit_rules: list[Rule]
    error: str = None
    

