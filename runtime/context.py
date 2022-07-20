import dataclasses
import re

from models.transaction import Tx
from models.action import BaseAction, SignType


@dataclasses.dataclass()
class BaseContext(object):
    action: BaseAction
    origin: str = dataclasses.field(init=False)
    sign_type: SignType = dataclasses.field(init=False)
    
    def __post_init__(self):
        self.origin = self.action.origin
    
    def is_null(self, obj):
        return False if obj else True

    def is_not_null(self, obj):
        return not self.is_null(obj)

    def is_in_list(self, obj, dest_list):
        return True if obj in dest_list else False

    def is_not_in_list(self, obj, dest_list):
        return not self.is_in_list(obj, dest_list)


@dataclasses.dataclass()
class TextContext(BaseContext):
    text: str = dataclasses.field(init=False)

    def __post_init__(self):
        super(TextContext, self).__post_init__()
        self.text = self.action.text
        self.sign_type = SignType.text

    def is_match_text_sign(self, text, text_sign_pattern):
        p = re.compile(text_sign_pattern)
        m = p.match(text)
        return True if m else False


@dataclasses.dataclass()
class TransactionContext(BaseContext):
    tx: Tx = dataclasses.field(init=False)
    
    def __post_init__(self):
        super(TransactionContext, self).__post_init__()
        self.tx = self.get_tx(self.action)
        self.sign_type = SignType.transaction

    def get_tx(self, action):
        tx = action.transaction
        if not tx:
            return
        return Tx(**dict(
            chain_id=tx['chainId'],
            data=tx.get('data', '0x'),
            from_=tx.get('from', '').lower(),
            to=tx.get('to', '').lower(),
            gas=int(tx.get('gas', '0x'), 16),
            gas_price=tx.get('gasPrice', 0),
            nonce=int(tx.get('nonce'), 16),
            value=int(tx.get('value'), 16)
        ))