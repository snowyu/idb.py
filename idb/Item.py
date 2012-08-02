# the abstract Item Class for iDB KeyValue Storage:
#
#
# myItem = Item.LoadFrom(path = '/dd/dff', key = 'myKey', cache=False)
#
#
from os import path

from utils import CreateDir, SetXattrValue, GetXattrValue
from helpers import IDB_SPEC_VER, WriteFileValueToCache, ReadFileValueFromCache, DeleteDBValue, iDBError
from helpers import EIDBNODIR, IDB_VALUE_NAME, IDB_KEY_TYPE_NAME


class Item(object):
    @staticmethod
    def get_options(**kwargs):
        result = {}
        kw_defaults = { 'path': '', 'cache': True, 'key': '' }
        for key, value in kw_defaults.iteritems():
            if kwargs.has_key(key):
                result[key] = kwargs[key]
            else:
                result[key] = value
        return result
    @classmethod
    def new_data(cls, aData):
        if aData  == None:
            aData = 0
        result = super(Item, cls).__new__(cls, aData)
        result.data = int(aData)
        return result
    @classmethod
    def new(cls,  aData, aNewFunc, **kwargs):
        result = aNewFunc(aData)
        # the path is the database path
        # the key is the list's key
        options = cls.get_options(** kwargs)
        for key, value in options.iteritems():
            setattr(result, key, value)
        if result.path  ==  '':
            raise iDBError(EIDBNODIR, 'Please specify the database directory first!')
        result.cache = bool(result.cache)
        return result
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
        WriteFileValueToCache(vDir, str(aValue), IDB_VALUE_NAME)
        WriteFileValueToCache(vDir, cls.__name__, IDB_KEY_TYPE_NAME)
    def LoadFromDir(self, aKey):
        # load the item from the aKey
        result = get_by_dir(self.path, aKey)
        if result != None:
            self.data = result
    def SaveToDir(self, aKey):
        self.set_by_dir(self.path, aKey, self)
    def LoadFromCache(self, aKey):
        result = get_by_cache(self.path, aKey)
        if result != None:
            self.data = result
    def SaveToCache(self, aKey):
        self.set_by_cache(self.path, aKey, self)
    @classmethod
    def LoadFrom(cls, **kwargs):
        options = cls.get_options(** kwargs)
        if options['path']  ==  '':
            raise iDBError(EIDBNODIR, 'Please specify the database directory first!')
        data = cls.get_by_dir(options['path'], options['key'])
        if data == None and options['cache']: 
          data = result.get_by_cache(options['path'], options['key'])
        if data  == None:
            raise iDBError(EIDBNOSUCHKEY, "Error: No Such Key(%s) Exists." % path.join(result.path, result.key))

        # create a new instance
        result  = cls(data,  ** kwargs)
        #result.data = data

        return result

    def SaveTo(self, aKey,  **kwargs):
        self.SaveToDir(aKey)
        cache = self.cache
        if kwargs.has_key('cache'):
            cache = kwargs['cache']
        if cache:
            self.SaveToCache(aKey)
    def Load(self):
        cache = self.cache
        if kwargs.has_key('cache'):
            cache = kwargs['cache']
        result = self.LoadFromDir(self.key)
        if not result and cache:
            result = self.LoadFromCache(self.key)
        if result  == None:
            raise iDBError(EIDBNOSUCHKEY, "Error: No Such Key(%s) Exists." % path.join(result.path, result.key))
        return result
    def Save(self):
        self.SaveTo(self.key)
    def Delete(self):
        delete(self.path, self.key)

    def __cast(self, other):
        if isinstance(other, Item): return other.data
        else: return other
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

