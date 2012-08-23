# The Dict Class(Spec v0.2):
# http://docs.python.org/reference/datamodel.html#special-method-names
# from Dict import Dict
# a=Dict({'hi':123, 'world': 45, 'goo': 'for good', 'tru': True}, path='test', key='myk')
# a.Save()
# b=Dict.LoadFrom(path='test', key='myk', loadOnDemand=False)
# 

import errno
from os import path
from glob import glob
from UserDict import DictMixin


from utils import ForceDirectories, SetXattr, GetXattr, IsXattrExists, ListXattr
from helpers import IDB_SPEC_VER, WriteValueFromFile, ReadValueFromFile, DeleteDBValue, iDBError
from helpers import EIDBNODIR, IDB_VALUE_NAME, IDB_KEY_TYPE_NAME

from Item import Item, Loading
from Integer import Integer
from Hex import Hex
from String import String
from Boolean import Boolean


# If you need to get a class from a module, you can use getattr: getattr(glob, 'glob')
# the class is in your scope:
#get_class = lambda x: globals()[x]

class Dict(Item, DictMixin):
    @property
    def loadOnDemand(self):
        return self._loadOnDemand
    @loadOnDemand.setter
    def loadOnDemand(self, value):
        self._loadOnDemand = bool(value)
    @classmethod
    def parse_options(cls, **kwargs):
        result = Item.parse_options(** kwargs)
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
    def get_by_xattr(aPath, aKey, ** kwargs):
        vDir = path.join(aPath, aKey)
        result = None
        vData = GetXattr(vDir, IDB_VALUE_NAME)
        if vData != None:
            result = {}
            vData = vData.strip().splitlines()
            for key in vData:
                 if len(key) and key[0] != '.':
                     if kwargs['loadOnDemand']:
                         result[key] = Loading(path=aPath, key=aKey)
                     else:
                         kwargs['key'] = aKey + '/' + key
                         result[key] = Item.LoadItem(** kwargs)
        return result
    @staticmethod
    def get_by_file(aPath, aKey, ** kwargs):
        result = None
        vDir = path.join(aPath, aKey)
        vData = ReadValueFromFile(vDir, IDB_VALUE_NAME)
        if len(vData):
            #vData = vData.strip()
            result = {}
            for key in vData:
                if len(key) and key[0] != '.':
                     result[key] = Loading(path=aPath, key=aKey)
        return result
    @classmethod
    def set_by_xattr(cls, aPath, aKey, aValue):
        # save the Integer to the aKey
        vDir = path.join(aPath, aKey)
        ForceDirectories(vDir)
        keys = ''
        opts = aValue.GetOptions()
        for key in aValue.data:
            v = aValue[key]
            if isinstance(v, Item):
                v.Save( ** opts)
                keys += key + '\n'
        #super(Dict, cls).set_by_xattr(vDir, keys)
        SetXattr(vDir, IDB_VALUE_NAME, keys)
        SetXattr(vDir, IDB_KEY_TYPE_NAME, cls.__name__)

    @classmethod
    def set_by_file(cls, aPath, aKey, aValue):
        vDir = path.join(aPath, aKey)
        keys = ''
        opts = aValue.GetOptions()
        for key in aValue.data:
            v = aValue[key]
            if isinstance(v, Item):
                v.Save( ** opts)
                keys += key + '\n'
        #super(Dict, cls).set_by_file(vDir, keys)
        WriteValueFromFile(vDir, keys, IDB_VALUE_NAME)
        WriteValueFromFile(vDir, cls.__name__, IDB_KEY_TYPE_NAME)


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
            if isinstance(result, Loading):
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
        elif isinstance(item, bool):
            item = Boolean(item,  ** opts)
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
