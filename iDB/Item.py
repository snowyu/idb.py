# the Item Class for iDB KeyValue Storage:
#
# Register your new Item Type by:
#    Item.Register(Dict)
#
# myItem = Item.LoadItem(path = '/dd/dff', key = 'myKey')
#
#
import urllib
from os import path

from utils import ForceDirectories, SetXattr, GetXattr, IsXattrExists
from helpers import IDB_SPEC_VER, WriteValueFromFile, ReadValueFromFile, DeleteDBValue, iDBError
from helpers import EIDBNOSUCHKEY, EIDBNODIR, IDB_VALUE_NAME, IDB_KEY_TYPE_NAME

class Loading():
    def __init__(self,  **kwargs):
        kw_defaults = {'path': '', 'key': ''}
        for key, value in kw_defaults.iteritems():
            if kwargs.has_key(key):
                value = kwargs[key]
            setattr(self, key, value)

class Item(object):
    _ItemClasses = {}
    @staticmethod
    def Register(aClass):
        Item._ItemClasses[aClass.__name__] = aClass
    @classmethod
    def LoadItem(cls, ** kwargs):
        ItemClasses = Item._ItemClasses
        vType = cls.GetType( ** kwargs )
        vTypeClass= ItemClasses[vType]
        return vTypeClass.LoadFrom(** kwargs)
    @classmethod
    def parse_options(cls, **kwargs):
        result = {}
        kw_defaults = { 'path': '', 'storeInXattr': True, 'storeInFile': True, 'key': '.' }
        for key, value in kw_defaults.iteritems():
            if kwargs.has_key(key):
                result[key] = kwargs[key]
            else:
                result[key] = value
        if result['key'] == '':
            result['key'] == '.'
        result['storeInXattr'] = bool(result['storeInXattr'])
        result['storeInFile'] = bool(result['storeInFile'])
        return result
    @classmethod
    def new_data(cls, aData):
        if aData  == None:
            aData = 0
        result = super(Item, cls).__new__(cls)
        result.data = aData
        return result
    def __new__(cls,  aData=None, **kwargs):
        return Item.new(aData, cls.new_data,  ** kwargs)
    @classmethod
    def new(cls,  aData, aNewFunc, **kwargs):
        result = aNewFunc(aData)
        # the path is the database path
        # the key is the list's key
        options = cls.parse_options(** kwargs)
        result.ApplyOptions( ** options)
        #for key, value in options.iteritems():
        #    setattr(result, '_' + key, value)
        if result.path  ==  '':
            raise iDBError(EIDBNODIR, 'Please specify the database directory first!')
        result.key = result._key
        return result
    @staticmethod
    def exists_by_xattr(aPath, aKey):
        vDir  = path.join(aPath, aKey)
        return IsXattrExists(vDir, IDB_VALUE_NAME)
    @staticmethod
    def exists_by_file(aPath, aKey):
        vFile = path.join(aPath, aKey, IDB_VALUE_NAME)
        return path.isfile(vFile)
    @staticmethod
    def delete(aPath, aKey):
        vDir  = path.join(aPath, aKey)
        DeleteDBValue(vDir)
    @staticmethod
    def get_by_xattr(aPath, aKey, aAttribute=IDB_VALUE_NAME, ** kwargs):
        # load the Integer from the aKey
        vDir = path.join(aPath, aKey)
        result = GetXattr(vDir, aAttribute)
        return result
    @classmethod
    def set_by_xattr(cls, aPath, aKey, aValue):
        # save the Integer to the aKey
        vDir = path.join(aPath, aKey)
        #ForceDirectories(vDir)
        SetXattr(vDir, IDB_VALUE_NAME, str(aValue))
        SetXattr(vDir, IDB_KEY_TYPE_NAME, cls.__name__)
    @staticmethod
    def get_by_file(aPath, aKey, aAttribute=IDB_VALUE_NAME, ** kwargs):
        vDir = path.join(aPath, aKey)
        result = ReadValueFromFile(vDir, aAttribute)
        if result != None:
            result = result[0]
        return result
    @classmethod
    def set_by_file(cls, aPath, aKey, aValue):
        vDir = path.join(aPath, aKey)
        WriteValueFromFile(vDir, str(aValue), IDB_VALUE_NAME)
        WriteValueFromFile(vDir, cls.__name__, IDB_KEY_TYPE_NAME)
    @property
    def key(self):
        return urllib.unquote(self._key)
    @key.setter
    def key(self, value):
        self._key = urllib.quote(value, '/ ')
    @property
    def path(self):
        return self._path
    @path.setter
    def path(self, value):
        self._path = value
    @property
    def storeInFile(self):
        return self._storeInFile
    @storeInFile.setter
    def storeInFile(self, value):
        self._storeInFile = bool(value)
    @property
    def storeInXattr(self):
        return self._storeInXattr
    @storeInXattr.setter
    def storeInXattr(self, value):
        self._storeInXattr = bool(value)
    # Get the current options to pass through
    # DO NOT INCLUDE path and key
    def GetOptions(self):
        result = dict(self._options)
        if result.has_key('path'):
            del result['path']
        if result.has_key('key'):
            del result['key']
        return result
    def ApplyOptions(self,  ** options):
        for key, value in options.iteritems():
            setattr(self, '_' + key, value)
        self._options = options

    @classmethod
    def GetType(cls,  ** kwargs):
        options = cls.parse_options(** kwargs)
        if options['path']  ==  '':
            raise iDBError(EIDBNODIR, 'Please specify the database directory first!')
        data = Item.get_by_xattr(options['path'], options['key'], IDB_KEY_TYPE_NAME)
        if data == None and options['storeInFile']:
            data = Item.get_by_file(options['path'], options['key'], IDB_KEY_TYPE_NAME)
        if data  == None:
            raise iDBError(EIDBNOSUCHKEY, "Error: No Such Key(%s) Exists." % path.join(options['path'], options['key']))

        return data

    def LoadFromXattr(self, aKey=None):
        # load the item from the aKey
        if aKey == None:
            aKey = self.key
        result = get_by_xattr(self.path, aKey)
        if result  == None:
            raise iDBError(EIDBNOSUCHKEY, "Error: No Such Key(%s) Exists." % path.join(self.path, self.key))
        self.data = self.__data__(result)
    def SaveToXattr(self, aKey=None):
        if aKey == None:
            aKey = self.key
        self.set_by_xattr(self.path, aKey, self)
    def LoadFromFile(self, aKey=None):
        if aKey == None:
            aKey = self.key
        result = self.get_by_file(self.path, aKey)
        if result  == None:
            raise iDBError(EIDBNOSUCHKEY, "Error: No Such Key(%s) Exists." % path.join(self.path, self.key))
        self.data = self.__data__(result)
    def SaveToFile(self, aKey=None):
        if aKey == None:
            aKey = self.key
        self.set_by_file(self.path, aKey, self)
    @classmethod
    def LoadFrom(cls, **kwargs):
        options = cls.parse_options(** kwargs)
        if options['path']  ==  '':
            raise iDBError(EIDBNODIR, 'Please specify the database directory first!')
        vData = None
        #vType = None #see LoadItem
        if options['storeInXattr']:
            vData = cls.get_by_xattr(options['path'], options['key'],  ** options)
            #vType = cls.get_by_xattr(options['path'], options['key'], IDB_KEY_TYPE_NAME)
        else:
            options['storeInFile'] = True
        if vData == None and options['storeInFile']:
            vData = cls.get_by_file(options['path'], options['key'],  ** options)
            #vType = cls.get_by_file(options['path'], options['key'], IDB_KEY_TYPE_NAME)
        if vData  == None:
            raise iDBError(EIDBNOSUCHKEY, "Error: No Such Key(%s) Exists." % path.join(options['path'], options['key']))

        # create a new instance
        result  = cls(cls.__data__(vData),  ** kwargs)
        #result.data = vData

        return result

    def SaveTo(self, aKey,  **kwargs):
        xattr = self.storeInXattr
        if kwargs.has_key('storeInXattr'):
            xattr = kwargs['storeInXattr']
        storeInFile = self.storeInFile
        if kwargs.has_key('storeInFile'):
            storeInFile = kwargs['storeInFile']
        vDir = path.join(self.path, aKey)
        ForceDirectories(vDir)
        if xattr:
            self.SaveToXattr(aKey)
        else:
            storeInFile = True
        if storeInFile:
            self.SaveToFile(aKey)
    def Load(self,  **kwargs):
        storeInFile = self.storeInFile
        if kwargs.has_key('storeInFile'):
            backup = kwargs['storeInFile']
        xattr = self.storeInXattr
        if kwargs.has_key('storeInXattr'):
            xattr = kwargs['storeInXattr']
        else:
            storeInFile = True
        result = None
        if xattr:
            result = self.LoadFromXattr(self.key)
        if not result and storeInFile:
            result = self.LoadFromFile(self.key)
        #if result  == None:
        #    raise iDBError(EIDBNOSUCHKEY, "Error: No Such Key(%s) Exists." % path.join(self.path, self.key))
        return result
    def Save(self,  **kwargs):
        self.SaveTo(self.key,  ** kwargs)
    def Delete(self):
        self.delete(self.path, self.key)
    def Exists(self):
        result = None
        if self.storeInXattr:
            result = self.exists_by_xattr(self.path, self.key)
        if not result and self.storeInFile:
            result = self.exists_by_file(self.path, self.key)
        return result
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
        return self.data >= value
    def __hash__(self):
        return self.data.__hash__()
    def __repr__(self):
        return str(self.data)
    def __cmp__(self, value):
        return cmp(self.data, value)
    # convert data to str
    def __str__(self):
        return str(self.data)
    # convert str to data
    @staticmethod
    def __data__(aStr):
        return aStr

