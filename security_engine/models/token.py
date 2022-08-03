import dataclasses
from .contract import Contract


@dataclasses.dataclass()
class Token(object):

    id: str
    name: str
    symbol: str
    decimals: int
    total_supply: int
    contract: Contract
