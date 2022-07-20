from enum import Enum
import typing
import dataclasses


class SignType(Enum):
    transaction = 1
    text = 2


@dataclasses.dataclass()
class BaseAction(object):
    sign_type: str = dataclasses.field(init=False)
    origin: str
    
    def __post_init__(self):
        pass

@dataclasses.dataclass()
class TransactionAction(BaseAction):
    chain_id: int = dataclasses.field(init=False)
    transaction: dict

    def __post_init__(self):
        super(TransactionAction, self).__post_init__()
        self.sign_type = SignType.transaction
        self.chain_id = self.transaction['chainId']


@dataclasses.dataclass()
class TextAction(BaseAction):

    text: str
    chain_id: int
        
    def __post_init__(self):
        super(TextAction, self).__post_init__()
        self.sign_type = SignType.text


def get_action(params):
    if SignType.transaction.name in params:
        action = TransactionAction(**params)
    elif SignType.text.name in params:
        action = TextAction(**params)
    else:
        return None
    return action



