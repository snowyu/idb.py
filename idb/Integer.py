# The Integer / KeyValue Class(Spec v0.2):
# http://docs.python.org/reference/datamodel.html#special-method-names

from utils import Str2Int
from Numberic import Numberic

class Integer(Numberic, int):
    @classmethod
    def new_data(cls, aData):
        if aData  == None:
            aData = 0
        result = super(Integer, cls).__new__(cls, aData)
        result.data = int(aData)
        return result
    # Int is immutable class, so I have to use __new__ classmethod.
    def __new__(cls,  aData, **kwargs):
        return Numberic.new(aData, cls.new_data,  ** kwargs)
    @staticmethod
    def get_by_dir(aPath, aKey):
        # load the Integer from the aKey
        result = Str2Int(Numberic.get_by_dir(aPath, aKey))
        return result
    @staticmethod
    def get_by_cache(aPath, aKey):
        result = Str2Int(Numberic.get_by_cache(aPath, aKey))
        return result

