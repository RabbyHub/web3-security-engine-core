class Item(dict):
    def __getattr__(self, k):
        return self[k]

    @classmethod
    def convert_from_dict(cls, dct: dict):
        ins = cls(**dct)
        for k, v in ins.items():
            if isinstance(v, dict):
                ins[k] = cls.convert_from_dict(v)
        return ins

