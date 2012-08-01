#!/usr/bin/python
#coding:utf-8

import string, random
import os
import errno

from os import path
from xattr import xattr

def RandomString(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def GetXattrValue(aFile, aKey):
    result = None
    x = xattr(aFile)
    try:
        result = x[aKey]
    except (KeyError, IOError) as e:
        if type(e) == IOError:
            if e.errno  != errno.ENOENT: # No Such File
                raise
    return result

def SetXattrValue(aFile, aKey, aValue):
    result = None
    x = xattr(aFile)
    try:
        x[aKey] = aValue
        result  = True
    except (KeyError, IOError) as e:
        if type(e) == IOError:
            if e.errno  != errno.ENOENT: # No Such File
                raise
    return result

def IsXattrValueExists(aFile, aKey):
    result = False
    x = xattr(aFile)
    try:
        result = x.has_key(aKey)
    except (KeyError, IOError) as e:
        if type(e) == IOError:
            if e.errno  != errno.ENOENT: # No Such File
                raise
    return result

# return the dir's count in aDir
def GetDirCount(aDir):
    return sum(1 for item in os.listdir(aDir) if path.isdir(path.join(aDir, item)))

# return the file's count in aDir
def GetFileCount(aDir):
    return sum(1 for item in os.listdir(aDir) if path.isfile(path.join(aDir, item)))

# Create all missed directoy 
def CreateDir(aDir):
    try:
        os.makedirs(aDir)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST:
            pass
        else: raise

def TouchFile(aFileName, aTimeStamp = None):
    #fhandle = 
    file(aFileName, 'a').close()
    if aTimeStamp != None:
        try:
            os.futimes(aFileName, aTimeStamp)
        except ENOSYS:
            os.utime(aFileName, aTimeStamp)
        #finally:
        #    fhandle.close()

# the Conversion functions:
def Str2Int(value):
    if value != None:
        base = 10
        if value[0]  == '$':
            value = value[1:]
            base = 16
        elif value[0:2] == '0x':
            value = value[2:]
            base = 16
        if value[0] == '"' and value[-1] == '"':
            value = [1:-1]
        elif value[0] == "'" and value[-1] == "'":
            value = [1:-1]
        result = int(value, base)
    else:
        result = None

    return result

def Str2Hex(value):
    if value[0]  == '$':
        value = value[1:]
    return int(value, 16)

def Hex2Str(value):
    return '$' + hex(value)[2:]

def Str2Bool(value):
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

