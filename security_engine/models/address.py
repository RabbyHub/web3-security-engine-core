import dataclasses
from typing import List
from .contract import Contract
from .chain import Chain


@dataclasses.dataclass()
class Address(object):
    id: str
    contract_list: List[Contract] = dataclasses.field(default_factory=list)
    used_chain_list: List[Chain] = dataclasses.field(default_factory=list)




