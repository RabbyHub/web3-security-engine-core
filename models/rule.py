import dataclasses
import typing
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
    conditions: typing.Optional(list[Condition])
    logic: str
    version: str  # github commit or tag


@dataclasses.dataclass()
class RuleHit(object):
    description: str
    level: str


@dataclasses.dataclass()
class ExecuteLog(object):
    origin: str
    text: str
    tx: Tx
    rule: Rule
    err: str
    hit: bool
    time_at: int
    

