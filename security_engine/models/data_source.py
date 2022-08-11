class DataSource(dict):

    def __getattr__(self, k):
        return self[k]

    @classmethod
    def from_dict(cls, dct: dict):
        ins = cls(**dct)
        return ins


class AddressSet(DataSource):
    pass

AddressSet.__name__ = 'address_set'

class DomainSet(DataSource):
    pass

DomainSet.__name__ = 'domain_set'


class SignTextPatternSet(DataSource):
    pass

SignTextPatternSet.__name__ = 'sign_text_pattern_set'