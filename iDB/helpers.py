#!/usr/bin/python
#coding:utf-8

import logging
import errno
import glob

import utils

from os import path
from shutil import rmtree
from xattr import xattr
from urllib import quote, unquote

from utils import Str2Hex, Str2Bool, ForceDirectories, TouchFile, GetXattr, IsXattrExists, SetXattr

# Constants
# the iDB Library version:
IDB_VER = '0.0.2'
# the iDB Specification version:
IDB_SPEC_VER = 1

IDB_KEY_TYPE_NAME = '.type'
IDB_VALUE_NAME    = '.value'
IDB_KEYS_NAME   = '.keys'

logger = logging.getLogger(__name__)


EIDBNODIR  =  -100 # No DB DIR Specified
EIDBKEYEXISTS = -101 # the Key is already Exists.
EIDBNOSUCHKEY = -102 # No Such Key is exists.

class iDBError(Exception):
    def __init__(self, errno, msg):
        self.errno  = errno
        self.message = msg
    def __str__(self):
        return repr(self.message)

def IsFileValueExists(aDir, aAttriubte=IDB_VALUE_NAME, aDBVersion=IDB_SPEC_VER):
    result = IsXattrExists(aDir, aAttriubte)
    if not result:
        aFile = path.join(aDir, aAttriubte)
        result = path.isfile(aFile)
    if not result and aDBVersion  <= 0.1 and aAttriubte == IDB_VALUE_NAME:  
        aFile = path.join(aDir, '=*')
        result = len(glob.glob(aFile)) > 0 # Search dir by pattern
    return result

def ReadValueFromFile(aDir, aAttriubte=IDB_VALUE_NAME):
    result = None
    vFile = path.join(aDir, aAttriubte)
    try:
        result = [line.strip() for line in open(vFile, 'r')]
    except IOError as e:
        if e.errno != errno.ENOENT: # No Such File
            raise
    return result
def ReadFileValue(aDir, aAttriubte=IDB_VALUE_NAME, aDBVersion=IDB_SPEC_VER):
    """
    """
    result = GetXattr(aDir, aAttriubte)
    if result == None:
        # It's the backup of the value.
        result = ReadValueFromFile(aDir, aAttriubte)
    else:
        result = [result]
    if result == None and aDBVersion <= 0.1 and aAttriubte == IDB_VALUE_NAME: # just keep backcompatible
        aFile = path.join(aDir, '=*')
        result = glob.glob(aFile) # Search dir by pattern
        result = [value.replace(path.join(aDir, '='),'') for value in result] #remove the prefix "="
    return result

def WriteValueFromFile(aDir, aValue, aAttriubte=IDB_VALUE_NAME):
    vFile = path.join(aDir, aAttriubte)
    with open(vFile, 'w') as f:
        f.write(aValue)

# the aDir MUST BE urllib.quote(aDir, '/') first!
# the aString MUST BE urllib.quote(aString) first!
def WriteFileValue(aDir, aValue, aAttriubte=IDB_VALUE_NAME, aBackup = True):
    """Create aString in aDir
    """
    #aFile = path.join(aDir, '=' + aString)
    #vDir = path.dirname(aFile)
    #aString = path.basename(aFile)
    ForceDirectories(aDir)
    SetXattr(aDir, aAttriubte, aValue)
    #TouchFile(aFile)
    if aBackup:
        WriteValueFromFile(aDir, aValue, aAttriubte)

def RemoveFileValue(aDir):
    rmtree(aDir)

# the Conversion functions:
IDB_TYPES = {'String': str, 'Object': dict, 'Integer': int, 'Hex': Str2Hex, 'Float': float, 'Boolean': Str2Bool}
IDB_LTYPES = {str: 'String', dict: 'Object', int: 'Integer', hex: 'Hex', float: 'Float', bool: 'Boolean'}

def String2FieldValue(aStr, aType):
    result = aStr
    if IDB_TYPES.has_key(aType):
        result = IDB_TYPES[aType](result)
    else:
        logger.warning("Field2String: Unkown Field Type '%s' treat as String type" % aType)
    return result

def FieldValue2String(aValue, aType):
    result = None
    if aType == 'Hex':
        result = hex(aValue)
    else:
        result = str(aValue)
    return result

# the helper functions to operate the iDB
def CreateDBValue(aDir, aValue, aValueType, aBackup = True, aDBVersion=IDB_SPEC_VER):
    """
    """
    if not IsFileValueExists(aDir, IDB_VALUE_NAME, aDBVersion):
        WriteFileValue(aDir, aValue, IDB_VALUE_NAME, aBackup)
        WriteFileValue(aDir, aValueType, IDB_KEY_TYPE_NAME, aBackup)
    else:
        raise iDBError(EIDBKEYEXISTS, "add key error: the key(%s) is already exists!" % aDir)

def UpdateDBValue(aDir, aValue, aValueType, aBackup = True, aDBVersion=IDB_SPEC_VER):
    if IsFileValueExists(aDir, IDB_VALUE_NAME, aDBVersion):
        WriteFileValue(aDir, aValue, IDB_VALUE_NAME, aBackup)
        WriteFileValue(aDir, aValueType, IDB_KEY_TYPE_NAME, aBackup)
    else:
        raise iDBError(EIDBNOSUCHKEY, "Update key error: No such key(%s) exists!" % aDir)

def PutDBValue(aDir, aValue, aValueType, aBackup = True, aDBVersion=IDB_SPEC_VER):
    WriteFileValue(aDir, aValue, IDB_VALUE_NAME, aBackup)
    WriteFileValue(aDir, aValueType, IDB_KEY_TYPE_NAME, aBackup)

def DeleteDBValue(aDir):
    RemoveFileValue(aDir)

def GetDBValue(aDir, aDBVersion=IDB_SPEC_VER):
    vValues = ReadFileValue(aDir, IDB_VALUE_NAME, aDBVersion)
    if len(vValues) > 0:
        # try to determine the value's type.
        vKeyType = ReadFileValue(aDir, IDB_KEY_TYPE_NAME, aDBVersion)
        if IDB_TYPES.has_key(vKeyType):
            vKeyType = IDB_TYPES[vKeyType]

        if len(vValues) == 1:
            vValues = vValues[0]
            if vKeyType == None: # guess the type of the value
                if vValues[0] == '$':
                    try:
                        vValues  = int(vValues[1:], 16)
                        vKeyType = 'Hex'
                    except ValueError:
                        pass
                if vKeyType == None:
                    if (vValues[i][0]  == '"' and vValues[i][-1]  == '"'):
                        vValues[i] = vValues[1:-1]
                        vKeyType = 'String'
                    elif (vValues[i][0]  == '\'' and vValues[i][-1]  == '\''):
                        vValues[i] = vValues[1:-1] # remove quote
                        vKeyType = 'String'

                if vKeyType == None:
                    try:
                        vValues  = int(vValues)
                        vKeyType = 'Integer'
                    except ValueError:
                        pass
                if vKeyType == None:
                    try:
                        vValues  = float(vValues)
                        vKeyType = 'Float'
                    except ValueError:
                        pass
                if vKeyType == None:
                    try:
                        vValues = Str2Bool(vValues)
                        vKeyType = 'Boolean'
                    except ValueError:
                        pass
                if vKeyType == None:
                    vKeyType = 'String'

                logger.warning("'%s' missing value type as '%s' added!" % aDir, vKeyType)
                WriteFileValue(aDir, vKeyType, IDB_KEY_TYPE_NAME)
            else:
                vValues = String2FieldValue(vValues)
        else: #multi-values here
            """
            """
        return vValues


