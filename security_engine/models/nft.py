import dataclasses
from .contract import Contract


@dataclasses.dataclass()
class NFT(object):
    id: str
    name: str
    inner_id: str
    is_erc721: bool
    is_erc1155: bool
    contract: Contract


class NFTCollection(object):
    id: str
    is_erc1155: bool
    is_erc721: bool
    contract: Contract
