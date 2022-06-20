import dataclasses
from .contract import Contract


@dataclasses.dataclass()
class Address(object):
    id: str
    contractList: list[Contract]
    usedChainList: list  # 是否放到 built func






