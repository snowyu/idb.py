# The String Class(Spec v0.2):

import operator
from Item import Item

class String(Item,  str):
    @classmethod
    def new_data(cls, aData):
        if aData  == None:
            aData = 0
        #result = super(String, cls).__new__(cls, aData)
        result = str.__new__(cls, aData)
        result.data = str(aData)
        return result
    #def __new__(cls,  aData, **kwargs):
    #    return Item.new(aData, cls.new_data,  ** kwargs)

    def __int__(self):
        return int(self.data)
    def __long__(self):
        return long(self.data)
    def __float__(self):
        return float(self.data)
    def __oct__(self):
        return oct(self.data)
    def __hex__(self):
        return hex(self.data)
    def __complex__(self):
        return complex(self.data)
    def __add__(self, value):
        result = self.data + value
        return type(self)(result, path=self.path, cache=self.cache, key=self.key)
    def __radd__(self, value):
        result = value + self.data
        return type(self)(result, path=self.path, cache=self.cache, key=self.key)
    @staticmethod
    def __data__(aStr):
        result = aStr.strip()
        if result[0] == '"' and result[-1] == '"':
            result = result[1:-1]
        elif result[0] == "'" and result[-1] == "'":
            result = result[1:-1]
        return result

Item.Register(String)
