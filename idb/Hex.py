# The Hex / KeyValue Class(Spec v0.2):

import os
import collections

from os import path

from utils import CreateDir, Str2Int, SetXattrValue, GetXattrValue
from helpers import IDB_SPEC_VER, WriteFileValueToCache, ReadFileValueFromCache, DeleteDBValue, iDBError
from helpers import EIDBNODIR, IDB_VALUE_NAME, IDB_KEY_TYPE_NAME
from Integer import Integer
from Item import Item

class Hex(Integer):
    #def __new__(cls,  aData, **kwargs):
    #    return Item.new(aData, Hex.new_data,  ** kwargs)
    def __str__(self):
        return hex(self.data)
    def __repr__(self):
        return hex(self.data)
 
