from models import Address, Token, Contract, TokenTransfer, TokenApprove, Chain
from funcs import reg


@reg.register
class CustomFuncMixin(object):

    def __init__(self, tx) -> None:
        self.tx = tx
        self._token_transfer = None
        self._token_approve = None
        self._chain = None
    
    def func_dict(self):
        return dict(
            getAddress=self.get_address,
            getToken=self.get_token,
            getContract=self.get_contract,
            getAddrToAddrTransferCount=self.get_addr_to_addr_transfer_count
        )

    def property_dict(self):
        return dict(
            tokenTransfer=self.token_transfer,
            tokenApprove=self.token_approve
        )

    @property
    def chain(self):
        return self._chain
    
    @chain.setter
    def chain(self):
        return Chain()
    
    @property
    def token_transfer(self):
        return self._token_transfer

    @token_transfer.setter
    def token_transfer(self):
        # parse self.tx.data
        return TokenTransfer()

    @property
    def token_approve(self):
        # parse self.tx.data
        return self._token_approve
        
    @token_approve.setter
    def token_approve(self):
        # parse self.tx.data
        return TokenApprove()

    def get_address(self, id):
        # todo add local cache
        return Address(id=id)
    
    def get_token(self, id):
        return Token(id=id)
    
    def get_contract(self, id, chain):
        return Contract(id=id, chain=chain)
    
    def get_addr_to_addr_transfer_count(self, from_, to, chain):
        return 0


