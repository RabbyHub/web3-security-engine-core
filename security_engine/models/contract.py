import dataclasses
from .chain import Chain
from .protocol import Protocol


@dataclasses.dataclass()
class Contract(object):
    id: str
    chain: Chain
    code_id: str
    creator: str
    is_token: bool
    is_suicide: bool
    is_multisig: bool
    protocol: Protocol

