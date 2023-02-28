from enum import Enum
import typing
import dataclasses


class SignType(Enum):
    transaction = 1
    text = 2
    typed_data = 3


@dataclasses.dataclass()
class BaseAction(object):
    sign_type: str = dataclasses.field(init=False)
    origin: str
    domain: str = dataclasses.field(init=False)
    def __post_init__(self):
        pass


@dataclasses.dataclass()
class TransactionAction(BaseAction):
    chain_id: int = dataclasses.field(init=False)
    transaction: dict

    def __post_init__(self):
        super(TransactionAction, self).__post_init__()
        self.sign_type = SignType.transaction
        self.chain_id = int(self.transaction['chainId'])


@dataclasses.dataclass()
class TextAction(BaseAction):
    
    chain_id: int
    text: str
        
    def __post_init__(self):
        super(TextAction, self).__post_init__()
        self.sign_type = SignType.text


@dataclasses.dataclass()
class TypedDataAction(BaseAction):

    chain_id: int = dataclasses.field(init=False)
    typed_data: dict
    
    def __post_init__(self):
        super(TypedDataAction, self).__post_init__()
        self.sign_type = SignType.typed_data
        self.chain_id = int(self.typed_data['domain']['chainId'])


def get_action(params):
    if SignType.transaction.name in params:
        action = TransactionAction(**params)
    elif SignType.text.name in params:
        action = TextAction(**params)
    elif SignType.typed_data.name in params:
        action = TypedDataAction(**params)
    else:
        return None
    return action



