import dataclasses


@dataclasses.dataclass()
class Chain(object):
    id: int
    uid: str # identity: str
    name: str


