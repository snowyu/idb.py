# the abstract Item Class for iDB KeyValue Storage:
#
#
#
from os import path

from helpers import IDB_SPEC_VER, WriteFileValueToCache, ReadFileValueFromCache, DeleteDBValue, iDBError
from helpers import EIDBNODIR, IDB_VALUE_NAME, IDB_KEY_TYPE_NAME


class Item(object):
    @staticmethod
    def new_data(aData):
        # create a new original data instance:
        # return int(aData)
        # THE DERIVIED CLASS MUST BE OVERRIDE
        return None
    @staticmethod
    def delete(aPath, aKey):
        vDir  = path.join(aPath, aKey)
        DeleteDBValue(vDir)
    @staticmethod
    def get_by_dir(aPath, aKey):
        # load the Integer from the aKey
        vDir = path.join(aPath, aKey)
        result = GetXattrValue(vDir, IDB_VALUE_NAME)
        return result
    @classmethod
    def set_by_dir(cls, aPath, aKey, aValue):
        # save the Integer to the aKey
        vDir = path.join(aPath, aKey)
        CreateDir(vDir)
        SetXattrValue(vDir, IDB_VALUE_NAME, str(aValue))
        SetXattrValue(vDir, IDB_KEY_TYPE_NAME, cls.__name__)
    @staticmethod
    def get_by_cache(aPath, aKey):
        vDir = path.join(aPath, aKey)
        result = ReadFileValueFromCache(vDir, IDB_VALUE_NAME)
        if result != None:
            result = result[0]
        return result
    @classmethod
    def set_by_cache(cls, aPath, aKey, aValue):
        vDir = path.join(aPath, aKey)
        WriteFileValueToCache(vDir, aValue, IDB_VALUE_NAME)
        WriteFileValueToCache(vDir, cls.__name__, IDB_KEY_TYPE_NAME)
    def LoadFromDir(self, aKey):
        # load the item from the aKey
        result = get_by_dir(self.path, aKey)
        if result != None:
            self.data = result
    def SaveToDir(self, aKey):
        self.set_by_dir(self.path, aKey, self.data)
    def LoadFromCache(self, aKey):
        result = get_by_cache(self.path, aKey)
        if result != None:
            self.data = result
    def SaveToCache(self, aKey):
        self.set_by_cache(self.path, aKey, self.data)
    @classmethod
    def LoadFrom(cls, aData, **kwargs):
        #result = super(Integer, cls).__new__(cls, aInt)
        result = cls.new_data(aData)
        # the path is the database path
        # the key is the list's key
        kw_defaults = {path: '', cache: True, key: ''}
        for key, value in kw_defaults.iteritems():
            if kwargs.has_key(key):
                val = kwargs[key]
            else:
                val = value
            setattr(result, key, val)
        data = get_by_dir(result.path, result.key)
        if data == None and result.cache: 
          data = get_by_cache(result.path, result.key)
        if data  == None:
            raise iDBError(EIDBNOSUCHKEY, "Error: No Such Key(%s) Exists." % path.join(result.path, result.key))
        result.data = data
        return result

    def SaveTo(self, aKey,  **kwargs):
        cache = self.cache
        if kwargs.has_key('cache'):
            cache = kwargs['cache']
        if cache:
            SaveToCache(self, aKey)
        SaveToDir(self, aKey)
    def Load(self):
        cache = self.cache
        if kwargs.has_key('cache'):
            cache = kwargs['cache']
        result = LoadFromDir(self, self.key)
        if not result and cache:
            result = LoadFromCache(self, self.key)
        if result  == None:
            raise iDBError(EIDBNOSUCHKEY, "Error: No Such Key(%s) Exists." % path.join(result.path, result.key))
        return result
    def Save(self):
        self.SaveTo(self.key)
    def Delete(self):
        delete(self.path, self.key)

    def __add__(self, value):
        result = self.data + value
        return type(self)(result, path=self.path, cache=self.cache, key=self.key)
    def __mul__(self, value):
        result = self.data * value
        return type(self)(result, path=self.path, cache=self.cache, key=self.key)
    def __mod__(self, value):
        result = self.data % value
        return type(self)(result, path=self.path, cache=self.cache, key=self.key)
    def __div__(self, value):
        result = self.data / value
        return type(self)(result, path=self.path, cache=self.cache, key=self.key)
    def __pow__(self, value):
        result = self.data  **  value
        return type(self)(result, path=self.path, cache=self.cache, key=self.key)
    def __neg__(self): # negation -self
        result = -self.data
        return type(self)(result, path=self.path, cache=self.cache, key=self.key)
    def __pos__(self): # Positive +self
        result = +self.data
        return type(self)(result, path=self.path, cache=self.cache, key=self.key)
    def __rshift__(self, value):
        result = self.data  >>  value
        return type(self)(result, path=self.path, cache=self.cache, key=self.key)
    def __lshift__(self, value):
        result = self.data  << value
        return type(self)(result, path=self.path, cache=self.cache, key=self.key)
    def __lt__(self, value):
        return self.data < value
    def __le__(self, value):
        return self.data <= value
    def __eq__(self, value):
        return self.data == value
    def __ne__(self, value):
        return self.data != value
    def __gt__(self, value):
        return self.data > value
    def __ge__(self, value):
        return self.data > value
    def __str__(self):
        return str(self.data)
    def __repr__(self):
        return str(self.data)
    def __cmp__(self, value):
        return cmp(self.data, value)

