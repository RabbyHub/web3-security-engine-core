import dataclasses
import re
from urllib.parse import urlparse
from security_engine.models.transaction import Tx
from security_engine.models.action import BaseAction, SignType
from security_engine.models.chain import Chain


@dataclasses.dataclass()
class BaseContext(object):
    action: BaseAction
    origin: str = dataclasses.field(init=False)
    domain: str = dataclasses.field(init=False)
    sign_type: SignType = dataclasses.field(init=False)
    chain: Chain = dataclasses.field(init=False)
    
    def __post_init__(self):
        self.origin = self.get_origin(self.action.origin)
        self.domain = self.get_domain(self.origin)
    
    def get_origin(self, origin):
        if not origin:
            return ''
        return origin.rstrip('/')

    def get_domain(self, origin):
        if not origin:
            return ''
        return urlparse(origin).netloc


@dataclasses.dataclass()
class TextContext(BaseContext):
    text: str = dataclasses.field(init=False)

    def __post_init__(self):
        super(TextContext, self).__post_init__()
        self.text = self.action.text
        self.sign_type = SignType.text

    def match_sign_text(self, text, text_sign_pattern):
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
            gas=int(tx.get('gas', '0x0'), 16),
            gas_price=int(tx.get('gasPrice', '0x0'), 16),
            max_fee_per_gas=int(tx.get('maxFeePerGas', '0x0'), 16),
            max_priority_fee_per_gas=int(tx.get('maxPriorityFeePerGas', '0x0'), 16),
            nonce=int(tx.get('nonce', '0x0'), 16),
            value=int(tx.get('value', '0x0'), 16)
        ))