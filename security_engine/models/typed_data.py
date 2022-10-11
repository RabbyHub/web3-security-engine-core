import dataclasses
import typing


@dataclasses.dataclass()
class TypedData(object):

    chain_id: int
    version: str
    name: str
    verifying_contract: str
    primary_type: str
    types: typing.Dict
    message: typing.Dict