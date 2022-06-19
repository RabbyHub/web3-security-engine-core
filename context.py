from funcs import reg
from models import Tx
from utils.item import Item


class Context(object):

    def __init__(self, activity, source=None):
        self.tx, self.text, self.origin = activity['transaction'], activity['text'], activity['origin']
        self.source = source
        self.local_ctx = Item(self.initalize())
        
    def initalize(self):
        self._local_ctx = dict(
            source=self.source,
            tx=self.format_tx(self.activity),
            origin=self.origin,
            text=self.text
        )
        for key in reg.keys:
            func_object = reg[key]()
            self._local_ctx.update(func_object().func_dict())
            self._local_ctx.update(func_object().property_dict())
        return self._local_ctx

    def format_tx(self, activity):
        tx = activity.get('transaction')
        if not tx:
            return
        # todo validate
        return Tx(**dict(
            chainId=tx['chainId'],
            data=tx.get('data', '0x'),
            from_=tx.get('from'),
            to=tx.get('to'),
            gas=int(tx.get('gas', '0x'), 16),
            gasPrice=tx.get('gasPrice', 0),
            nonce=int(tx.get('nonce'), 16),
            value=int(tx.get('value'), 16)
        ))
         


    