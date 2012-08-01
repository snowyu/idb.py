# The Integer / KeyValue Class(Spec v0.2):

import os
import collections

from os import path

from utils import CreateDir, Str2Int, SetXattrValue, GetXattrValue
from helpers import IDB_SPEC_VER, WriteFileValueToCache, ReadFileValueFromCache, DeleteDBValue, iDBError
from helpers import EIDBNODIR, IDB_VALUE_NAME, IDB_KEY_TYPE_NAME
from Item import Item


class Integer(int, Item):
    @staticmethod
    def new_data(aData):
        if aData:
            result = int(aData)
        else:
            result = int()
        return result
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
    @staticmethod
    def get_by_dir(aPath, aKey):
        # load the Integer from the aKey
        result = Str2Int(Item.get_by_dir(aPath, aKey))
        return result
    @staticmethod
    def get_by_cache(aPath, aKey):
        result = Str2Int(Item.get_by_cache(aPath, aKey))
        return result
 
