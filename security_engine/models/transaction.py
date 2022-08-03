import dataclasses
import typing

# transaction
@dataclasses.dataclass()
class Tx(object):
    
    chain_id: int
    from_: str
    to: str
    value: int
    data: bytes
    gas: int
    nonce: int
    gas_price: typing.Optional[int]
    max_fee_per_gas: typing.Optional[int] = 0
    max_priority_fee_per_gas: typing.Optional[int] = 0



