import dataclasses
import typing
from .token import Token
from .nft import NFT, NFTCollection
from .contract import Contract


@dataclasses.dataclass()
class TokenTransfer(object):
    from_addr: str
    to: str
    token: Token
    amount: int


@dataclasses.dataclass()
class TokenApprove(object):
    onwer: str
    spender: str
    spender_contract: typing.Optional[Contract]
    token: Token
    amount: int


@dataclasses.dataclass()
class NFTTransfer(object):
    _from: str
    to: str
    nft: NFT
    amount: int


@dataclasses.dataclass()
class NFTApprove(object):
    owner: str
    spender: str
    spender_contract: typing.Optional[Contract]
    nft: NFT
    amount: int


@dataclasses.dataclass()
class NFTCollectionApprove(object):
    onwer: str
    spender: str
    spender_contract: typing.Optional[Contract]
    nft_collection: NFTCollection
    amount: int