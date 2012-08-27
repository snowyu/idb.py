# The Integer / KeyValue Class:
# http://docs.python.org/reference/datamodel.html#special-method-names

from utils import Str2Int
from Item import Item
from Numberic import Numberic

class Integer(Numberic, int):
    @classmethod
    def new_data(cls, aData):
        if aData  == None:
            aData = 0
        #result = super(Integer, cls).__new__(cls, aData)
        result = int.__new__(cls, aData)
        result.data = int(aData)
        return result
    # Int is immutable class, so I have to use __new__ classmethod.
    #def __new__(cls,  aData, **kwargs):
    #    return Numberic.new(aData, cls.new_data,  ** kwargs)
    @staticmethod
    def __data__(aStr):
        return Str2Int(aStr)

Item.Register(Integer)
