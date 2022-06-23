from functools import cached_property, cache
from runtime.context import Context
from models.transaction_scene import TokenTransfer, TokenApprove, NFTApprove, NFTCollectionApprove
from models.token import Token
from models.address import Address


class CustomContext(Context):

    def __init__(self, activity):
        super(CustomContext, self).__init__(activity)

    @cached_property
    def token_transfer(self):
        return TokenTransfer()

    @cached_property
    def token_approve(self):
        return TokenApprove()

    @cached_property
    def nft_approve(self):
        return NFTApprove()

    @cached_property
    def nft_collection_approve(self):
        return NFTCollectionApprove()

    @cache
    def get_token(self, id):
        return Token()
    
    @cache
    def get_address(self, id):
        return Address()


    