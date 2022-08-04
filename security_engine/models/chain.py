import dataclasses


@dataclasses.dataclass()
class Chain(object):
    id: str  # identifier, eg. eth, arb
    network_id: int = 0
    name: str = ''


