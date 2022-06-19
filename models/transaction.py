import dataclasses
import typing

# transaction

@dataclasses.dataclass()
class Tx(object):
    
    chain_id: int
    from_addr: str
    to: str
    value: int
    data: bytes
    gas: int
    nonce: int
    gas_price: typing.Optional[int]
    max_fee_per_gas: typing.Optional[int]
    max_priority_fee_per_gas: typing.Optional[int]



