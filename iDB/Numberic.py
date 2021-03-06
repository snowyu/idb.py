# The Abstract Numberic Class:
# http://docs.python.org/reference/datamodel.html#special-method-names

import operator
from Item import Item

class Numberic(Item):
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
    def __abs__(self):
        return abs(self.data)
    def __neg__(self): # negation -self
        result = -self.data
        return type(self)(result, ** self._options)
    def __pos__(self): # Positive +self
        result = +self.data.pos
        return type(self)(result, ** self._options)
    def __invert__(self):
        return operator.invert(self.data)

    def __add__(self, value):
        result = self.data + value
        return type(self)(result, ** self._options)
    def __sub__(self, value):
        result = self.data - value
        return type(self)(result, ** self._options)
    def __mul__(self, value):
        result = self.data * value
        return type(self)(result, ** self._options)
    def __mod__(self, value):
        result = self.data % value
        return type(self)(result, ** self._options)
    def __div__(self, value):
        result = self.data / value
        return type(self)(result, ** self._options)
    def __truediv__(self, value):
        result = operator.truediv(self.data, value)
        return type(self)(result, ** self._options)
    def __floordiv__(self, value):
        result = self.data // value
        return type(self)(result, ** self._options)
    def __divmod__(self, value):
        result = divmod(self.data, value)
        return type(self)(result, ** self._options)
    def __pow__(self, value):
        result = self.data  **  value
        return type(self)(result, ** self._options)
    def __rshift__(self, value):
        result = self.data  >>  value
        return type(self)(result, ** self._options)
    def __lshift__(self, value):
        result = self.data  << value
        return type(self)(result, ** self._options)
    def __and__(self, value):
        result = operator.and_(self.data,  value)
        return type(self)(result, ** self._options)
    def __xor__(self, value):
        result = operator.xor(self.data,  value)
        return type(self)(result, ** self._options)
    def __or__(self, value):
        result = operator.or_(self.data,  value)
        return type(self)(result, ** self._options)
    def __radd__(self, value):
        result = self.data + value
        return type(self)(result, ** self._options)
    def __rsub__(self, value):
        result = self.data - value
        return type(self)(result, ** self._options)
    def __rmul__(self, value):
        result = self.data * value
        return type(self)(result, ** self._options)
    def __rmod__(self, value):
        result = self.data % value
        return type(self)(result, ** self._options)
    def __rdiv__(self, value):
        result = self.data / value
        return type(self)(result, ** self._options)
    def __rtruediv__(self, value):
        result = operator.truediv(self.data, value)
        return type(self)(result, ** self._options)
    def __rfloordiv__(self, value):
        result = self.data // value
        return type(self)(result, ** self._options)
    def __rdivmod__(self, value):
        result = divmod(self.data, value)
        return type(self)(result, ** self._options)
    def __rpow__(self, value):
        result = self.data  **  value
        return type(self)(result, ** self._options)
    def __rrshift__(self, value):
        result = self.data  >>  value
        return type(self)(result, ** self._options)
    def __rlshift__(self, value):
        result = self.data  << value
        return type(self)(result, ** self._options)
    def __rand__(self, value):
        result = operator.and_(self.data,  value)
        return type(self)(result, ** self._options)
    def __rxor__(self, value):
        result = operator.xor(self.data,  value)
        return type(self)(result, ** self._options)
    def __ror__(self, value):
        result = operator.or_(self.data,  value)
        return type(self)(result, ** self._options)

