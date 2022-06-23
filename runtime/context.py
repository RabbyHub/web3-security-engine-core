from functools import cached_property
from models.transaction import Tx


class BaseContext(dict):

    def __init__(self):
        pass

    def add_property(self, key, value):
        self[key] = value
        
    def add_property_dict(self, **kwargs):
        self.update(**kwargs)


class Context(BaseContext):

    def __init__(self, activity, data_source=None):
        self.data_source = data_source
        self.activity = activity
        super(Context, self).__init__()

    @cached_property
    def origin(self):
        origin = self.activity.get('origin')
        return origin

    @cached_property
    def text(self):
        text = self.activity.get('text')
        return text
        
    @cached_property
    def tx(self):
        tx = self.activity.get('transaction')
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
         
    def is_null(self, obj):
        return False if obj else True

    def is_not_null(self, obj):
        return not self.is_null(obj)

    def is_in_list(self, obj, dest_list):
        return True if obj in dest_list else False

    def is_not_in_list(self, obj, dest_list):
        return not self.is_in_list(obj, dest_list)


    