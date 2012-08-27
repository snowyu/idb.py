# The Float / KeyValue Class:

from Item import Item
from Numberic import Numberic

class Float(Numberic, float):
    @classmethod
    def new_data(cls, aData):
        if aData  == None:
            aData = 0
        result = float.__new__(cls, aData)
        result.data = float(aData)
        return result
    @staticmethod
    def __data__(aStr):
        return float(aStr)

Item.Register(Float)
