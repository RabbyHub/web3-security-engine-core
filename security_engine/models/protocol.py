import dataclasses


@dataclasses.dataclass()
class Protocol(object):
    id: str
    name: str
    logo_url: str