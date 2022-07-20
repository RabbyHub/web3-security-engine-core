import dataclasses
from enum import Enum
from .action import BaseAction, SignType

DATA_SOURCE = 'data_source'
COMMON_ORIGIN = 'common'


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


@dataclasses.dataclass()
class App(object):
    name: str
    rules: list[Rule]
    data_source: object
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
    action: BaseAction
    app: App
    hit_rules: list[Rule]
    time_at: int
    error: str = None
    

