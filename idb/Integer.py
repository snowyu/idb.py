# The Integer / KeyValue Class(Spec v0.2):

import os
import collections

from os import path

from utils import CreateDir, Str2Int, SetXattrValue, GetXattrValue
from helpers import IDB_SPEC_VER, WriteFileValueToCache, ReadFileValueFromCache, DeleteDBValue, iDBError
from helpers import EIDBNODIR, IDB_VALUE_NAME, IDB_KEY_TYPE_NAME


class Integer(int):
    # Int is immutable class, so I have to use new classmethod.
    def __new__(cls,  aInt, **kwargs):
        result = super(Integer, cls).__new__(cls, aInt)
        # the path is the database path
        # the key is the list's key
        kw_defaults = {path: '', cache: True, key: ''}
        for key, value in kw_defaults.iteritems():
            if kwargs.has_key(key):
                val = kwargs[key]
            else:
                val = value
            setattr(result, key, val)
        if result.path  ==  '':
            raise iDBError(EIDBNODIR, 'Please specify the database directory first!')
        result.cache = bool(result.cache)
        result.data = int(aInt)
        return result
    def __add__(self, value):
        result = int.__add__(self.data, value)
        return type(self)(result, path=self.path, cache=self.cache, key=self.key)
    def __mul__(self, value):
        result = int.__mul__(self.data, value)
        return type(self)(result, path=self.path, cache=self.cache, key=self.key)
    def __mod__(self, value):
        result = int.__mod__(self.data, value)
        return type(self)(result, path=self.path, cache=self.cache, key=self.key)
    def __div__(self, value):
        result = int.__div__(self.data, value)
        return type(self)(result, path=self.path, cache=self.cache, key=self.key)
    def __pow__(self, value):
        result = int.__pow__(self.data, value)
        return type(self)(result, path=self.path, cache=self.cache, key=self.key)
    def __neg__(self): # negation -self
        result = int.__neg__(self.data)
        return type(self)(result, path=self.path, cache=self.cache, key=self.key)
    def __pos__(self): # Positive +self
        result = int.__pos__(self.data)
        return type(self)(result, path=self.path, cache=self.cache, key=self.key)
    def __rshift__(self, value):
        result = int.__rshift__(self.data, value)
        return type(self)(result, path=self.path, cache=self.cache, key=self.key)
    def __lshift__(self, value):
        result = int.__lshift__(self.data, value)
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

    @staticmethod
    def delete(aPath, aKey):
        vDir  = path.join(aPath, aKey)
        DeleteDBValue(vDir)
    @staticmethod
    def get_by_dir(aPath, aKey):
        # load the Integer from the aKey
        vDir = path.join(aPath, aKey)
        result = GetXattrValue(vDir, IDB_VALUE_NAME)
        result = Str2Int(result)
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
            result = Str2Int(result)
        return result
    @classmethod
    def set_by_cache(cls, aPath, aKey, aValue):
        vDir = path.join(aPath, aKey)
        WriteFileValueToCache(vDir, aValue, IDB_VALUE_NAME)
        WriteFileValueToCache(vDir, cls.__name__, IDB_KEY_TYPE_NAME)
    def LoadFromDir(self, aKey):
        # load the Integer from the aKey
        self.data = get_by_dir(self.path, aKey)
    def SaveToDir(self, aKey):
        self.set_by_dir(self.path, aKey, self.data)
    def LoadFromCache(self, aKey):
        result = get_by_cache(self.path, aKey)
        if result != None:
            self.data = result
    def SaveToCache(self, aKey):
        self.set_by_cache(self.path, aKey, self.data)
    def LoadFrom(self, aKey,  **kwargs):
        cache = self.cache
        if kwargs.has_key('cache'):
            cache = kwargs['cache']
        result = None
        if cache:
            result = LoadFromCache(self, aKey)
        if not result:
            result = LoadFromDir(self, aKey)
        return result
    def SaveTo(self, aKey,  **kwargs):
        cache = self.cache
        if kwargs.has_key('cache'):
            cache = kwargs['cache']
        if cache:
            SaveToCache(self, aKey)
        SaveToDir(self, aKey)
    def Load(self):
        self.LoadFrom(self.key)
    def Save(self):
        self.SaveTo(self.key)
    def Delete(self):
        delete(self.path, self.key)

