import dataclasses
from .chain import Chain


@dataclasses.dataclass()
class Contract(object):
    id: str
    chain: Chain
    code_id: str
    creator: str
    is_token: bool
    is_susicide: bool
    is_multisig: bool

