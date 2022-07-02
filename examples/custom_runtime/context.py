from functools import cached_property, cache
from runtime.context import Context
from models.transaction_scene import TokenTransfer, TokenApprove, NFTApprove, NFTCollectionApprove
from models.token import Token
from models.address import Address


class CustomContext(Context):

    def __init__(self, action):
        super(CustomContext, self).__init__(action)

    @cached_property
    def token_transfer(self):
        return None

    @cached_property
    def token_approve(self):
        return TokenApprove(onwer='0xB8c77482e45F1F44dE1745F52C74426C631bDD52', spender='0xB8c77482e45F1F44dE1745F52C74426C631bDD52', spender_contract=None, token=None, amount=1)

    @cached_property
    def nft_approve(self):
        return None

    @cached_property
    def nft_collection_approve(self):
        return None

    @cache
    def get_token(self, id):
        return Token(id='0xB8c77482e45F1F44dE1745F52C74426C631bDD52', name='BNB', symbol='BNB', decimals=18, total_supply=100000, contract=None)
    
    @cache
    def get_address(self, id):
        return None


    