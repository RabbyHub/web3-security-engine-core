import dataclasses


@dataclasses.dataclass()
class Chain(object):
    network_id: int
    id: str  # identifier, eg. eth, arb
    name: str = ''


