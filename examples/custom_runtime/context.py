import dataclasses
from security_engine.models.action import SignType
from security_engine.models.chain import Chain
from security_engine.runtime.context import TransactionContext, TextContext, TypedDataContext
from security_engine.models.sign_scene import TokenTransfer, TokenApprove, NFTApprove, NFTCollectionApprove


@dataclasses.dataclass()
class CustomTransactionContext(TransactionContext):

    token_transfer: TokenTransfer = None
    token_approve: TokenApprove = None
    nft_approve: NFTApprove = None
    nft_collection_approve: NFTCollectionApprove = None
    domain: str = None

    def __post_init__(self):
        super(CustomTransactionContext, self).__post_init__()
    
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
    
    def get_origin_set_of_text_sign(self, text):
        return ''


@dataclasses.dataclass()
class CustomTypedDataContext(TypedDataContext):
    
    token_approve: TokenApprove = None

    def __post_init__(self):
        super(CustomTypedDataContext, self).__post_init__()
    

def get_context(action):
    if action.sign_type == SignType.transaction:
        return CustomTransactionContext(action)
    elif action.sign_type == SignType.text:
        return CustomTextContext(action)
    elif action.sign_type == SignType.typed_data:
        return CustomTypedDataContext(action)
