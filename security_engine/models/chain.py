import dataclasses


@dataclasses.dataclass()
class Chain(object):
    id: int
    identifier: str
    name: str = ''


