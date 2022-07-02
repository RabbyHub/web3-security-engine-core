from urllib.parse import urlparse
from functools import cached_property
from models.transaction import Tx


class Context(object):

    def __init__(self, action):
        self.action = action
        super(Context, self).__init__()

    @cached_property
    def action(self):
        return self.action

    @cached_property
    def origin(self):
        origin = self.action.get('origin')
        return origin

    @cached_property
    def domain(self):
        if not self.origin:
            return
        return urlparse(self.origin).netloc

    @cached_property
    def text(self):
        text = self.action.get('text')
        return text
        
    @cached_property
    def tx(self):
        tx = self.action.get('transaction')
        if not tx:
            return
        # todo validate
        return Tx(**dict(
            chain_id=tx['chainId'],
            data=tx.get('data', '0x'),
            from_=tx.get('from'),
            to=tx.get('to'),
            gas=int(tx.get('gas', '0x'), 16),
            gas_price=tx.get('gasPrice', 0),
            nonce=int(tx.get('nonce'), 16),
            value=int(tx.get('value'), 16)
        ))
         
    def is_null(self, obj):
        return False if obj else True

    def is_not_null(self, obj):
        return not self.is_null(obj)

    def is_in_list(self, obj, dest_list):
        return True if obj in dest_list else False

    def is_not_in_list(self, obj, dest_list):
        return not self.is_in_list(obj, dest_list)


    