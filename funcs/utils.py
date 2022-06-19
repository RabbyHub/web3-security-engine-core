from funcs import reg

reg.register
class UtilFuncMixin(object):

    def __init__(self) -> None:
        pass

    def func_dict(self):
        return dict(
            isNull=self.is_null,
            isNotNull=self.is_not_null,
            isInList=self.is_in_list,
            isNotInlist=self.is_not_in_list
        )
    
    def property_dict(self):
        return {}

    def is_null(self, obj):
        return False if obj else True

    def is_not_null(self, obj):
        return not self.isNull(obj)

    def is_in_list(self, obj, destList):
        return True if obj in destList else False

    def is_not_in_list(self, obj, destList):
        return not self.isInList(obj, destList)
