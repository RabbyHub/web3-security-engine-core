import dataclasses
from security_engine.models.action import SignType
from security_engine.models.chain import Chain
from security_engine.runtime.context import TransactionContext, TextContext
from security_engine.models.sign_scene import TokenTransfer, TokenApprove, NFTApprove, NFTCollectionApprove
from security_engine.models.token import Token
from security_engine.models.address import Address


@dataclasses.dataclass()
class CustomTransactionContext(TransactionContext):

    token_transfer: TokenTransfer = None
    nft_approve: NFTApprove = None
    nft_collection_approve: NFTCollectionApprove = None


    def __post_init__(self):
        super(CustomTransactionContext, self).__post_init__()
    
    def token_approve(self):
        return TokenApprove(onwer='0xB8c77482e45F1F44dE1745F52C74426C631bDD52', spender='0xB8c77482e45F1F44dE1745F52C74426C631bDD52', spender_contract=None, token=None, amount=1)

    def nft_approve(self):
        return None

    def nft_collection_approve(self):
        return None

    def get_token(self, id):
        return Token(id='0xB8c77482e45F1F44dE1745F52C74426C631bDD52', name='DEMO', symbol='BNB', decimals=18, total_supply=100000, contract=None)
    
    def get_address(self, id):
        return None


@dataclasses.dataclass()
class CustomTextContext(TextContext):
    
    def __post_init__(self):
        super(CustomTextContext, self).__post_init__()
    

def get_context(action):
    if action.sign_type == SignType.transaction:
        return CustomTransactionContext(action)
    elif action.sign_type == SignType.text:
        return CustomTextContext(action)
