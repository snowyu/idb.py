# The Dict Class(Spec v0.2):
# http://docs.python.org/reference/datamodel.html#special-method-names
# from Dict import Dict
# a=Dict({'hi':123, 'world': 45, 'goo': 'for good', 'tru': True}, path='test', key='myk')
# a.Save()
# b=Dict.LoadFrom(path='test', key='myk', loadOnDemand=False)
# 

import errno
from os import path
from xattr import xattr
from glob import glob
from UserDict import DictMixin


from utils import CreateDir, SetXattrValue, GetXattrValue, IsXattrValueExists, GetXattrKeys
from helpers import IDB_SPEC_VER, WriteFileValueToBackup, ReadFileValueFromBackup, DeleteDBValue, iDBError
from helpers import EIDBNODIR, IDB_VALUE_NAME, IDB_KEY_TYPE_NAME

from Item import Item
from Integer import Integer
from Hex import Hex
from String import String



# If you need to get a class from a module, you can use getattr: getattr(glob, 'glob')
# the class is in your scope:
#get_class = lambda x: globals()[x]

class Loading():
    pass
class Dict(Item, DictMixin):
    @property
    def loadOnDemand(self):
        return self._loadOnDemand
    @loadOnDemand.setter
    def loadOnDemand(self, value):
        self._loadOnDemand = bool(value)
    @classmethod
    def get_options(cls, **kwargs):
        result = Item.get_options(** kwargs)
        kw_defaults = { 'loadOnDemand': True}
        for key, value in kw_defaults.iteritems():
            if kwargs.has_key(key):
                result[key] = kwargs[key]
            else:
                result[key] = value
        return result
    def GetOptions(self):
        result = super(Dict, self).GetOptions()
        result['loadOnDemand'] = self.loadOnDemand
        return result
    def update(self, aDict=None, **kwargs):
        if aDict is None:
            pass
        elif isinstance(aDict, Dict):
            aDict = aDict.data
        elif not isinstance(aDict, type({})) and hasattr(aDict, 'items'):
            aDict = aDict.items()
        for k, v in aDict.iteritems():
            self[k] = v
    @classmethod
    def new_data(cls, aData,  ** kw ):
        if aData  == None:
            aData = {}
        #result = super(UserDict, cls).__new__(cls, aData)
        result = object.__new__(cls)
        result.data = dict(aData)
        return result
    def __new__(cls,  aData=None, **kwargs):
        result = Dict.new(aData, cls.new_data,  ** kwargs)
        result.update(result.data)
        return result

    @staticmethod
    def get_by_dir(aPath, aKey):
        # load the Integer from the aKey
        vDir = path.join(aPath, aKey)
        result = None
        vData = GetXattrValue(vDir, IDB_VALUE_NAME)
        if vData != None:
            result = {}
            vData = vData.strip().splitlines()
            for key in vData:
                 if len(key) and key[0] != '.':
                     result[key] = Loading
        return result
    @staticmethod
    def get_by_backup(aPath, aKey):
        result = None
        vDir = path.join(aPath, aKey)
        vData = ReadFileValueFromBackup(vDir, IDB_VALUE_NAME)
        if len(vData):
            vData = vData.strip()
            result = {}
            for key in vData:
                if len(key) and key[0] != '.':
                     result[key] = Loading
        return result
    @classmethod
    def set_by_dir(cls, aPath, aKey, aValue):
        # save the Integer to the aKey
        vDir = path.join(aPath, aKey)
        CreateDir(vDir)
        keys = ''
        opts = aValue.GetOptions()
        for key in aValue.data:
            v = aValue[key]
            if isinstance(v, Item):
                v.Save( ** opts)
                keys += key + '\n'
        SetXattrValue(vDir, IDB_VALUE_NAME, keys)
        SetXattrValue(vDir, IDB_KEY_TYPE_NAME, cls.__name__)

    @classmethod
    def set_by_backup(cls, aPath, aKey, aValue):
        vDir = path.join(aPath, aKey)
        keys = ''
        opts = aValue.GetOptions()
        for key in aValue.data:
            v = aValue[key]
            if isinstance(v, Item):
                v.Save( ** opts)
                keys += key + '\n'
        WriteFileValueToBackup(vDir, keys, IDB_VALUE_NAME)
        WriteFileValueToBackup(vDir, cls.__name__, IDB_KEY_TYPE_NAME)


    # dict override:
    def __str__(self):
        if isinstance(self, dict):
            str(self)
        else:
             str(self.data)
    def __len__(self): return len(self.data)
    def __getitem__(self, key):
        if key in self.data:
            result = self.data[key]
            if result == Loading:
                opts = self.GetOptions()
                opts['path'] = self.path
                opts['key'] = self.key + '/' + key
                result = self.LoadItem( ** opts )
                self.data[key] = result
            return result
        if hasattr(self.__class__, "__missing__"):
            return self.__class__.__missing__(self, key)
        raise KeyError(key)

    def __setitem__(self, key, item):
        opts = self.GetOptions()
        opts['path'] = self.path
        opts['key'] = self.key + '/' + key
        #clsname = type(item).__name__
        if isinstance(item, Hex):
            item = Hex(item,  ** opts)
        elif isinstance(item, int): #int and Integer etc all derived from int.
            item = Integer(item,  ** opts)
        elif isinstance(item, str):
            item = String(item,  ** opts)
        elif isinstance(item, dict):
            item = Dict(item,  ** opts)
        elif item == Loading and not self.loadOnDemand:
            item = self.LoadItem(** opts)

        self.data[key] = item
    def __delitem__(self, key):
        vItem = self.data[key]
        if isinstance(vItem, Item):
            vItem.Delete()
        del self.data[key]
    def __iter__(self):
        return self.data.__iter__()
    def __reversed__(self):
        return self.data.__reversed__()
    def __contains__(self, item):
        return self.data.__contains__(item)
    def clear(self):
        for key in self.data.keys():
            vItem = self.data[key]
            if isinstance(vItem, Item):
                vItem.Delete()
            del self.data[key]
    def copy(self):
        if self.__class__ is Dict:
            return Dict(self.data.copy())
        import copy
        data = self.data
        try:
            self.data = {}
            c = copy.copy(self)
        finally:
            self.data = data
        c.update(self)
        return c
    def keys(self): return self.data.keys()
    def items(self): return self.data.items()
    def iteritems(self): return self.data.iteritems()
    def iterkeys(self): return self.data.iterkeys()
    def itervalues(self): return self.data.itervalues()
    def values(self): return self.data.values()
    def has_key(self, key): return key in self.data
    def pop(self, key, *args): return self.data.pop(key,  * args)

Item.Register(Dict)
