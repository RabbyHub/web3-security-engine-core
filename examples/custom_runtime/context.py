import dataclasses
from security_engine.models.action import SignType
from security_engine.models.chain import Chain
from security_engine.runtime.context import TransactionContext, TextContext
from security_engine.models.sign_scene import TokenTransfer, TokenApprove, NFTApprove, NFTCollectionApprove


@dataclasses.dataclass()
class CustomTransactionContext(TransactionContext):

    token_transfer: TokenTransfer = None
    nft_approve: NFTApprove = None
    nft_collection_approve: NFTCollectionApprove = None


    def __post_init__(self):
        super(CustomTransactionContext, self).__post_init__()
    
    def token_approve(self):
        # todo get token_approve property
        return None

    def nft_approve(self):
        # todo get nft_approve property
        return None

    def nft_collection_approve(self):
        # todo get nft_collection_approve property
        return None

    def get_token(self, id):
        # todo implement the get_token method
        return None
    
    def get_address(self, id):
        # todo Implement the get_address method
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
