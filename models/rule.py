import dataclasses
import typing


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
class RuleResult(object):
    description: str
    level: str

