#!/usr/bin/python
#coding:utf-8

import os
import sys, errno
import glob
from os import path

from utils import ForceDirectories
from helpers import IDB_SPEC_VER, GetDBValue, CreateDBValue, UpdateDBValue, PutDBValue, DeleteDBValue, iDBError
from helpers import EIDBNODIR
from Item import Item
from Dict import Dict
from Object import Object

class iValue(object):
    def __init__(self, aType, aValue):
        self.ValueType = aType
        self.value = aValue

class iDB(object):
    @classmethod
    def parse_options(cls, **kwargs):
        result = {}
        kw_defaults = {'path': '', 'storeInXattr': True, 'storeInFile': True, 'loadOnDemand': True, 'pageSize': 200}
        for key, value in kw_defaults.iteritems():
            if kwargs.has_key(key):
                result[key] = kwargs[key]
            else:
                 result[key] = value
        result['storeInXattr'] = bool(result['storeInXattr'])
        result['storeInFile'] = bool(result['storeInFile'])
        return result
    # Get the current options to pass through
    def GetOptions(self):
        result = dict(self._options)
        del result['path']
        return result
    def _ApplyOptions(self,  ** options ):
        for key, value in options.iteritems():
            setattr(self, '_' + key, value)
    def ApplyOptions(self,  ** new_options):
        opts = self._options 
        for key, value in new_options.iteritems():
            if opts.has_key(key):
                opts[key] = new_options[key]
                setattr(self, '_' + key, value)
    def __init__(self,  **kwargs):
        options = self.parse_options(** kwargs)
        self._options = options
        self._ApplyOptions(** options)
        self._version = IDB_SPEC_VER
        self.opened  = False


        #self.version = self.Get('.db/version')
        #if self.version  == None:
        #    self.version = IDB_SPEC_VER

    # Open database
    def Open(self, aSkipDBConfig = False):
        if self.path  ==  '':
            raise iDBError(EIDBNODIR, 'Please specify the database directory first!')
        vMetaInfo = Dict(path=self.path, key='.db', storeInFile=True, storeInXattr=False)
        if vMetaInfo.Exists():
            vMetaInfo.Load()
            self._version = vMetaInfo['version']
            #if vMetaInfo.has_key('version')
            if not aSkipDBConfig:
                self.ApplyOptions(**  vMetaInfo['config']);
        else:
            vMetaInfo['config'] = self.GetOptions()
            vMetaInfo['version']  =  self.version
            vMetaInfo.Save()

        self.opened = True
    def Close(self):
        if self.opened:
            vMetaInfo = Dict(path=self.path, key='.db', storeInFile=True, storeInXattr=False)
            vMetaInfo['config'] = self.GetOptions()
            vMetaInfo['version']  =  self.version
            vMetaInfo.Save()
            self.opened = False
    def Get(self, aKey):
        """return the value of the key
        """
        if not self.opened: return None
        opts = self.GetOptions()
        opts['path'] = self.path
        opts['key'] = akey
        result =  Item.LoadItem(** opts)
        return result.data

    def Put(self, aKey, aValue):
        """
        """
        if not self.opened: return None
        opts = self.GetOptions()
        opts['path'] = self.path
        opts['key'] = akey
        if isinstance(aValue, bool):
            aValue = Boolean(aValue,  ** opts)
        elif isinstance(aValue, int): #int and Integer etc all derived from int.
            aValue = Integer(aValue,  ** opts)
        elif isinstance(aValue, str):
            aValue = String(aValue,  ** opts)
        elif isinstance(aValue, dict):
            aValue = Dict(aValue,  ** opts)
        elif isinstance(aValue, Loading):
            opts['key'] = Loading.key
            aValue = self.LoadItem(path=Loading.path, key=Loading.key, loadOnDemand=False)
        elif isinstance(aValue, Item):
            aValue = type(aValue)(aValue.data,  ** opts)
        else:
            aValue = None
        if aValue != None:
            aValue.Save()
        return aValue != None

    def Delete(self, key):
        """
        """
        if not self.opened: return None
        vDir = path.join(self.path, key)
        DeleteDBValue(vDir)
    def WildcardSearch(self, aKeyPattern, aPage=0,  aPageSize=0):
        """aKeyPattern to Search the key through wildcard(*?) matching
           aPage is page number from 0 beginning.
           aPageSize is 0 means use the system default page size.
           retrun the matched keys list, pageNo and totalCount.
        """
        if not self.opened: return None
        vPath = path.join(self.path, aKeyPattern)

        result = []
        if aPageSize <= 0 or aPageSize > self.pageSize:
            aPageSize = self.pageSize
        vRoot  = path.join(self.path, '')
        vCount = 0
        vPage  = 0
        for vFile in glob.iglob(vPath):
            if path.isdir(vFile):
                vCount += 1
                vPage  =  vCount / aPageSize
                if vPage == aPage:
                    result += vFile.replace(vRoot, '')
                #elif vPage > aPage:
                #    break
        return {"count": vCount, "page": aPage, "result": result}
    def RegExSearch(self, aKeyPattern, aPage=0,  aPageSize=0):
        """aKeyPattern to Search the key through Regular Expressions matching.
           aPageNo is page number from 0 beginning.
           aPageSize is 0 means use the system default page size.
           retrun the matched keys list.
        """
        if not self.opened: return None
    @property
    def version(self):
        return self._version
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
    @property
    def loadOnDemand(self):
        return self._loadOnDemand
    @loadOnDemand.setter
    def loadOnDemand(self, value):
            self._loadOnDemand = bool(value)

