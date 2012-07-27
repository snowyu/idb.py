#!/usr/bin/python
#coding:utf-8

import utils
import errno
import glob

from os import path
from shutil import rmtree
from xattr import xattr
from urllib import quote_plus, unquote_plus

from utils import Str2Hex, Str2Bool, CreateDir, TouchFile

# Constants
# the iDB Library version:
IDB_VER = '0.0.2'
# the iDB Specification version:
IDB_SPEC_VER = '0.2'

IDB_KEY_TYPE = '.type'
IDB_VALUE_FILE = '.value'
IDB_TYPES = {'string': str, 'object': dict, 'integer': int, 'hex': Str2Hex, 'float': float, 'boolean': Str2Bool}
IDB_LTYPES = {str: 'String', dict: 'Object', int: 'Integer', hex: 'Hex', float: 'Float', bool: 'Boolean'}

IDB_ESCAPE_CHARS   = u'/*?'
IDB_UNESCAPE_CHARS = u'／＊？'

def EscapeChar(aChar, index=0):
    #for i, c in enumerate(IDB_ESCAPE_CHARS):
    for i in range(index, len(IDB_ESCAPE_CHARS)):
        if aChar == IDB_ESCAPE_CHARS[i]:
            aChar = IDB_UNESCAPE_CHARS[i]
            break
    return aChar

def UnEscapeChar(aChar index=0):
    #for i, c in enumerate(IDB_UNESCAPE_CHARS):
    for i in range(index, len(IDB_UNESCAPE_CHARS)):
        if aChar == IDB_UNESCAPE_CHARS[i]:
            aChar = IDB_ESCAPE_CHARS[i]
            break
    return aChar

def EscapeString(value, index=0):
    value = ''.join(EscapeChar(c, index) for c in value)
    return value

def UnEscapeString(value, index=0):
    value = ''.join(UnEscapeChar(c, index) for c in value)
    return value

def GetFileValue(aDir):
    """
    """
    result = None
    x = xattr(aDir)
    try:
        result = x[IDB_VALUE_FILE]
    except KeyError:
        pass
    if result == None:
        # It's backup only now in xattr version.
        aFile = path.join(aDir, IDB_VALUE_FILE)
        print("%s"  % aFile)
        try:
            result = [line.strip() for line in open(aFile, 'r')]
        except IOError, e:
            if e.errno != errno.ENOENT: # No Such File
                raise
    if result == None: # just keep backcompatible
        aFile = path.join(aDir, '=*')
        result = glob.glob(aFile) # Search dir by pattern
        result = [value.replace(path.join(aDir, '='),'') for value in result] #remove the prefix "="
    return result

def CreateDBString(aDir, aString, aCached = True):
    """Create aString in aDir
    """
    aFile = path.join(aDir, '=' + aString)
    vDir = path.dirname(aFile)
    aString = path.basename(aFile)
    CreateDir(vDir)
    TouchFile(aFile)
    if aCached:
        aFile = path.join(aDir, IDB_VALUE_FILE)
        with open(aFile, 'w') as f:
            f.write(aString)

# the helper functions to operate the iDB
def CreateDBValue(aDir,  aValue, aValueType):
    """
    """
def GetDBValue(aDir):
    vValues = GetFileValue(aDir) # Search dir by pattern
    if len(vValues) > 0:
        # try to determine the value's type.
        vKeyTypeDir = path.join(aDir, IDB_KEY_TYPE)
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
                        vKeyType = hex
                    except ValueError:
                        pass
                if vKeyType == None:
                    if (vValues[i][0]  == '"' and vValues[i][-1]  == '"'):
                        vValues[i] = vValues[1:-1]
                        vKeyType = str
                    elif (vValues[i][0]  == '\'' and vValues[i][-1]  == '\''):
                        vValues[i] = vValues[1:-1]
                        vKeyType = str

                if vKeyType == None:
                    try:
                        vValues  = int(vValues)
                        vKeyType = int
                    except ValueError:
                        pass
                if vKeyType == None:
                    try:
                        vValues  = float(vValues)
                        vKeyType = float
                    except ValueError:
                        pass
                if vKeyType == None:
                    try:
                        vValues = Str2Bool(vValues)
                        vKeyType = bool
                    except ValueError:
                        pass
                if vKeyType == None:
                    vKeyType = str
                    # remove quote if any
                    for i, value in enumerate(vValues):
                        if vValues[i][0]  == '"' and vValues[i][-1]  == '"':
                            vValues[i] = vValues[1:-1]
                        elif vValues[i][0]  == '\'' and vValues[i][-1]  == '\'':
                            vValues[i] = vValues[1:-1]

                CreateDBString(vKeyTypeDir, IDB_LTYPES[vKeyType])
            else:
                vValues = vKeyType(vValues)
        return vValues


