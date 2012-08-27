# The Hex / KeyValue Class:

from Item import Item
from Integer import Integer

class Hex(Integer):
    #def __new__(cls,  aData, **kwargs):
    #    return Item.new(aData, Hex.new_data,  ** kwargs)
    def __str__(self):
        return hex(self.data)
    def __repr__(self):
        return hex(self.data)

Item.Register(Hex)
