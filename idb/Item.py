# the abstract Item Class for iDB KeyValue Storage:
#
#
# myItem = Item.LoadFrom(path = '/dd/dff', key = 'myKey', backup=False)
#
#
import urllib
from os import path

from utils import CreateDir, SetXattrValue, GetXattrValue, IsXattrValueExists
from helpers import IDB_SPEC_VER, WriteFileValueToBackup, ReadFileValueFromBackup, DeleteDBValue, iDBError
from helpers import EIDBNODIR, IDB_VALUE_NAME, IDB_KEY_TYPE_NAME

class Item(object):
    _ItemClasses = {}
    @staticmethod
    def Register(aClass):
        Item._ItemClasses[aClass.__name__] = aClass
    @classmethod
    def LoadItem(cls, ** kwargs):
        ItemClasses = Item._ItemClasses
        vType = cls.GetItemType( ** kwargs )
        vClass= ItemClasses[vType]
        return vClass.LoadFrom( ** kwargs )
    @classmethod
    def get_options(cls, **kwargs):
        result = {}
        kw_defaults = { 'path': '', 'backup': True, 'key': '.' }
        for key, value in kw_defaults.iteritems():
            if kwargs.has_key(key):
                result[key] = kwargs[key]
            else:
                result[key] = value
        if result['key'] == '':
            result['key'] == '.'
        return result
    @classmethod
    def new_data(cls, aData):
        if aData  == None:
            aData = 0
        result = super(Item, cls).__new__(cls, aData)
        result.data = int(aData)
        return result
    def __new__(cls,  aData=None, **kwargs):
        return Item.new(aData, cls.new_data,  ** kwargs)
    @classmethod
    def new(cls,  aData, aNewFunc, **kwargs):
        result = aNewFunc(aData)
        # the path is the database path
        # the key is the list's key
        options = cls.get_options(** kwargs)
        result.ApplyOptions( ** options)
        #for key, value in options.iteritems():
        #    setattr(result, '_' + key, value)
        if result.path  ==  '':
            raise iDBError(EIDBNODIR, 'Please specify the database directory first!')
        result.backup = result._backup
        result.key = result._key
        return result
    @staticmethod
    def exists_by_dir(aPath, aKey):
        vDir  = path.join(aPath, aKey)
        return IsXattrValueExists(vDir, IDB_VALUE_NAME)
    def exists_by_backup(aPath, aKey):
        vFile = path.join(aPath, aKey, IDB_VALUE_NAME)
        return path.isfile(vFile)
    @staticmethod
    def delete(aPath, aKey):
        vDir  = path.join(aPath, aKey)
        DeleteDBValue(vDir)
    @staticmethod
    def get_by_dir(aPath, aKey, aAttribute=IDB_VALUE_NAME):
        # load the Integer from the aKey
        vDir = path.join(aPath, aKey)
        result = GetXattrValue(vDir, aAttribute)
        return result
    @classmethod
    def set_by_dir(cls, aPath, aKey, aValue):
        # save the Integer to the aKey
        vDir = path.join(aPath, aKey)
        CreateDir(vDir)
        SetXattrValue(vDir, IDB_VALUE_NAME, str(aValue))
        SetXattrValue(vDir, IDB_KEY_TYPE_NAME, cls.__name__)
    @staticmethod
    def get_by_backup(aPath, aKey, aAttribute=IDB_VALUE_NAME):
        vDir = path.join(aPath, aKey)
        result = ReadFileValueFromBackup(vDir, aAttribute)
        if result != None:
            result = result[0]
        return result
    @classmethod
    def set_by_backup(cls, aPath, aKey, aValue):
        vDir = path.join(aPath, aKey)
        WriteFileValueToBackup(vDir, str(aValue), IDB_VALUE_NAME)
        WriteFileValueToBackup(vDir, cls.__name__, IDB_KEY_TYPE_NAME)
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
    def backup(self):
        return self._backup
    @backup.setter
    def backup(self, value):
        self._backup = bool(value)
    # Get the current options to pass through
    def GetOptions(self):
        return {'backup': self._backup}
    def ApplyOptions(self,  ** options):
        for key, value in options.iteritems():
            setattr(self, '_' + key, value)

    @classmethod
    def GetItemType(cls,  ** kwargs):
        options = cls.get_options(** kwargs)
        if options['path']  ==  '':
            raise iDBError(EIDBNODIR, 'Please specify the database directory first!')
        data = Item.get_by_dir(options['path'], options['key'], IDB_KEY_TYPE_NAME)
        if data == None and options['backup']:
            data = Item.get_by_backup(options['path'], options['key'], IDB_KEY_TYPE_NAME)
        if data  == None:
            raise iDBError(EIDBNOSUCHKEY, "Error: No Such Key(%s) Exists." % path.join(options['path'], options['key']))

        return data

    def LoadFromDir(self, aKey=None):
        # load the item from the aKey
        if aKey == None:
            aKey = self.key
        result = get_by_dir(self.path, aKey)
        if result  == None:
            raise iDBError(EIDBNOSUCHKEY, "Error: No Such Key(%s) Exists." % path.join(self.path, self.key))
        self.data = self.__data__(result)
    def SaveToDir(self, aKey=None):
        if aKey == None:
            aKey = self.key
        self.set_by_dir(self.path, aKey, self)
    def LoadFromBackup(self, aKey=None):
        if aKey == None:
            aKey = self.key
        result = get_by_backup(self.path, aKey)
        if result  == None:
            raise iDBError(EIDBNOSUCHKEY, "Error: No Such Key(%s) Exists." % path.join(self.path, self.key))
        self.data = self.__data__(result)
    def SaveToBackup(self, aKey=None):
        if aKey == None:
            aKey = self.key
        self.set_by_backup(self.path, aKey, self)
    @classmethod
    def LoadFrom(cls, **kwargs):
        options = cls.get_options(** kwargs)
        if options['path']  ==  '':
            raise iDBError(EIDBNODIR, 'Please specify the database directory first!')
        data = cls.get_by_dir(options['path'], options['key'])
        if data == None and options['backup']:
            data = cls.get_by_backup(options['path'], options['key'])
        if data  == None:
            raise iDBError(EIDBNOSUCHKEY, "Error: No Such Key(%s) Exists." % path.join(options['path'], options['key']))

        # create a new instance
        result  = cls(cls.__data__(data),  ** kwargs)
        #result.data = data

        return result

    def SaveTo(self, aKey,  **kwargs):
        self.SaveToDir(aKey)
        backup = self.backup
        if kwargs.has_key('backup'):
            backup = kwargs['backup']
        if backup:
            self.SaveToBackup(aKey)
    def Load(self,  **kwargs):
        backup = self.backup
        if kwargs.has_key('backup'):
            backup = kwargs['backup']
        result = self.LoadFromDir(self.key)
        if not result and backup:
            result = self.LoadFromBackup(self.key)
        if result  == None:
            raise iDBError(EIDBNOSUCHKEY, "Error: No Such Key(%s) Exists." % path.join(result.path, result.key))
        return result
    def Save(self,  **kwargs):
        self.SaveTo(self.key,  ** kwargs)
    def Delete(self):
        delete(self.path, self.key)
    def Exists(self):
        result = self.exists_by_dir(self.path, self.key)
        if not result and self.backup:
            result = self.exists_by_backup(self.path, self.key)
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
        return self.data > value
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

