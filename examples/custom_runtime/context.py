import dataclasses
from functools import cached_property, cache
from models.action import SignType
from models.chain import Chain
from runtime.context import TransactionContext, TextContext
from models.transaction_scene import TokenTransfer, TokenApprove, NFTApprove, NFTCollectionApprove
from models.token import Token
from models.address import Address


@dataclasses.dataclass()
class CustomTransactionContext(TransactionContext):

    chain: Chain = dataclasses.field(init=False)
    token_transfer: TokenTransfer = None
    nft_approve: NFTApprove = None
    nft_collection_approve: NFTCollectionApprove = None


    def __post_init__(self):
        super(CustomTransactionContext, self).__post_init__()
        self.chain = self.get_chain(self.action.chain_id)
    
    @property
    def chain_map(self):
        return {
            1: {
                'network_id': 1,
                'identifier': 'eth',
                'name': 'Ethereum'
            },
            56: {
                'network_id': 56,
                'identifier': 'bsc',
                'name': 'BSC'
            }
        }

    # def token_transfer(self):
    #     return None

    def token_approve(self):
        return TokenApprove(onwer='0xB8c77482e45F1F44dE1745F52C74426C631bDD52', spender='0xB8c77482e45F1F44dE1745F52C74426C631bDD52', spender_contract=None, token=None, amount=1)

    def nft_approve(self):
        return None

    def nft_collection_approve(self):
        return None

    def get_chain(self, chain_id):
        if chain_id in self.chain_map:
            return Chain(id=chain_id, identifier=self.chain_map[id]['identifier'], name=self.chain_map[id]['name'])
        return None

    def get_token(self, id):
        return Token(id='0xB8c77482e45F1F44dE1745F52C74426C631bDD52', name='BNB', symbol='BNB', decimals=18, total_supply=100000, contract=None)
    
    def get_address(self, id):
        return None


@dataclasses.dataclass()
class CustomTextContext(TextContext):

    chain: Chain = dataclasses.field(init=False)
    
    def __post_init__(self):
        super(CustomTextContext, self).__post_init__()
        self.chain = self.get_chain(self.action.chain_id)
    
    @property
    def chain_map(self):
        return {
            1: {
                'network_id': 1,
                'identifier': 'eth',
                'name': 'Ethereum'
            },
            56: {
                'network_id': 56,
                'identifier': 'bsc',
                'name': 'BSC'
            }
        }

    def get_chain(self, chain_id):
        if chain_id in self.chain_map:
            return Chain(id=chain_id, identifier=self.chain_map[chain_id]['identifier'], name=self.chain_map[chain_id]['name'])
        return None


def get_context(action):
    if action.sign_type == SignType.transaction:
        return CustomTransactionContext(action)
    elif action.sign_type == SignType.text:
        return CustomTextContext(action)
