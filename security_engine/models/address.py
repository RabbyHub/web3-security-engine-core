import dataclasses
from .contract import Contract


@dataclasses.dataclass()
class Address(object):
    id: str
    contract_list: list[Contract]
    used_chain_list: list  # 是否放到 built func






