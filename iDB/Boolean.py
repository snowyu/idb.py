# The Hex / KeyValue Class(Spec v0.2):

from utils import Str2Bool
from Item import Item
from Integer import Integer

class Boolean(Item):
    @classmethod
    def new_data(cls, aData):
        if isinstance(aData, str):
            aData = Str2Bool(aData)
        else:
            aData = bool(aData)
        #result = int.__new__(cls, aData)
        #result.data = int(aData)
        return super(Boolean, cls).new_data(aData) #result
    #def __new__(cls,  aData, **kwargs):
    #    return Item.new(aData, Hex.new_data,  ** kwargs)
    def __str__(self):
        result = 'False'
        if self.data:
            result = 'True'
        return result
    def __repr__(self):
        return self.__str__()
    @staticmethod
    def __data__(aStr):
        return Str2Bool(aStr)

Item.Register(Boolean)
