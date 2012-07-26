#!/usr/bin/python
#coding:utf-8

#import os
from os import makedirs, path
import sys, errno
import glob
#import shutil
from shutil import rmtree
import string, random

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def mkdir_p(path):
    try:
        makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST:
            pass
        else: raise

def str2hex(value):
    return int(value, 16)

def str2bool(value):
    """
    Converts 'something' to boolean. Raises exception if it gets a string it doesn't handle.
    Case is ignored for strings. These string values are handled:
      True: 'True', "TRue", "yes", "y", "t"
      False: "", "faLse", "no", "n", "f"
    #Non-string values are passed to bool.
    """
    #if type(value) == type(''):
    if value.lower() in ("yes", "y", "true",  "t", ):
        return True
    if value.lower() in ("no",  "n", "false", "f"):
        return False
    raise ValueError('Invalid value for boolean conversion: ' + value)
    #return bool(value)

# Constants
# the iDB Library version:
IDB_VER = '0.0.1'
# the iDB Specification version:
IDB_SPEC_VER = '0.1'

IDB_KEY_TYPE = '.type'
IDB_VALUE_FILE = '=*'
IDB_TYPES = {'string': str, 'object': dict, 'integer': int, 'hex': str2hex, 'float': float, 'boolean': str2bool}
IDB_LTYPES = {str: 'String', dict: 'Object', int: 'Integer', str2hex: 'Hex', float: 'Float', str2bool: 'Boolean'}

# No DB DIR Specified
EIDBNODIR  =  -100

class iDBError(Exception):
    def __init__(self, errno, msg):
        self.errno  = errno
        self.message = msg
    def __str__(self):
        return repr(self.message)

class iValue(object):
    def __init__(self, aType, aValue):
        self.ValueType = aType
        self.value = aValue

def DBValue2Str(aValue):
    """
    """
def Str2DBValue(aStr, aType):
    """
    """
def AddDBValue(aDir, aValue):
    """
    """
# the helper functions to operate the iDB
def GetDBValue(aDir):
    vValues = path.join(aDir, IDB_VALUE_FILE)
    vValues = glob.glob(vValue) # Search dir by pattern
    if len(vValues) > 0:
        for i, value in enumerate(vValues):
            vValues[i] = value[1:]
        vKeyTypeDir = path.join(vDir, IDB_KEY_TYPE)
        vKeyType = None
        if path.exists(vKeyTypeDir):
            value = glob.glob(path.join(vKeyTypeDir, IDB_VALUE_FILE))
            if len(value) > 0:
                value = str.lower(value[0])
                if IDB_TYPES.has_key(value):
                    vKeyType = IDB_TYPES[value]
        if len(vValues) == 1:
            vValues = vValues[0]
            if vKeyType == None: # guess the type of the value
                if vValues[0] == '$':
                    try:
                        vValues  = int(vValues[1:], 16)
                        vKeyType = str2hex
                    except ValueError:
                        pass
                if vKeyType == None:
                    try:
                        vValues  = int(vValues)
                        vKeyType = int
                    except ValueError:
                        pass
                if vKeyType == None:
                    try:
                        vValues  = float(vValues)
                    except ValueError:
                        pass
                if vKeyType == None:
                    try:
                        vValues = str2bool(vValues)
                    except ValueError:
                        pass
                if vKeyType == None:
                    vKeyType = str
                AddDBValue(vKeyTypeDir, IDB_LTYPES[vKeyType])
            else:
                vValues = vKeyType(vValues)
        return vValues


class iDB(object):
    """
    """
    def __init__(self, db_dir):
        if db_dir  ==  '':
            raise iDBError(EIDBNODIR, 'Please specify the database directory first!')
        else:
            db_dir = db_dir
            mkdir_p(db_dir)
            self.root = db_dir
            self.version = self.Get('.db/version')
            if self.version  == None:
                self.version = IDB_SPEC_VER
"""
    def _TryHexGet(aValue):
        result = None
        if aValue[0] == '$':
            try:
                result = int(aValue[1:], 16)
            except ValueError:
                pass
        return result
"""

    def Get(self, key):
        """return the value of the key
        """
        vDir = path.join(self.root, key)
        return GetDBValue(vDir)

    def Add(self, key, value):
        """
        """
    def Update(self, key, value):
        """
        """
    def Put(self, key, value):
    def Delete(self, key):
    