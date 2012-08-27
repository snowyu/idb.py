# The Object / KeyValue Class:
# obj = Object.LoadFrom(path='test', key='myobj')
# obj.myattr

from Item import Item
from Dict import Dict

class Object(Dict):
    def __getattr__(self, name):
        if name <> 'data' and isinstance(self.data, dict) and self.data.has_key(name):
            return self.__getitem__(name)

    def __setattr__(self, name, value):
        if name <> 'data' and isinstance(self.data, dict) and self.data.has_key(name):
            return self.__setitem__(name, value)
        else:
            super(Object, self).__setattr__(name, value)


Item.Register(Object)
