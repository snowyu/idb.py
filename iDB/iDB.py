#!/usr/bin/python
#coding:utf-8

import os
import sys, errno
import glob
from os import path

from utils import ForceDirectories
from helpers import IDB_SPEC_VER, GetDBValue, CreateDBValue, UpdateDBValue, PutDBValue, DeleteDBValue, iDBError
from helpers import EIDBNODIR

class iValue(object):
    def __init__(self, aType, aValue):
        self.ValueType = aType
        self.value = aValue

class iDB(object):
    def _get(self, aKey, aValueType):
        """
        """
    def __init_parms__(self,  **kwargs):
        kw_defaults = {path: '', storeInFile: True,  storeInXattr: True}
        for key, value in kw_defaults.iteritems():
            if kwargs.has_key(key):
                val = kwargs[key]
            else:
                val = value
            setattr(self, '_' + key, val)
        self._backup  = bool(self._backup)
        self._version = IDB_SPEC_VER
        self.opened  = False
        #if self.path  ==  '':
        #    raise iDBError(EIDBNODIR, 'Please specify the database directory first!')

    def __init__(self,  **kwargs):
        """Open an existed database:
        iDB(path='/mydb', backup=True)
        """
        self.__init_parms__(** kwargs)


        #self.version = self.Get('.db/version')
        #if self.version  == None:
        #    self.version = IDB_SPEC_VER

    # Open database
    def Open(self, aSkipDBConfig = False):
        if self.path  ==  '':
            raise iDBError(EIDBNODIR, 'Please specify the database directory first!')
        if path.isdir(self.path):
            self.LoadDBMetaInfo(aSkipDBConfig)
        else:
            ForceDirectories(self.path)
            self.SaveDBMetaInfo()
        self.opened = True
    def SaveDBMetaInfo(self):
        self.Put('.db/version', self.version, 'Float')
    def Get(self, key):
        """return the value of the key
        """
        vDir = path.join(self.path, key)
        return GetDBValue(vDir, self.version)

    def Add(self, key, value):
        """
        """
        vDir = path.join(self.path, key)

        CreateDBValue(vDir, aValue, aValueType, self.cache, self.version)
    def Update(self, key, value):
        """
        """
        vDir = path.join(self.path, key)

        UpdateDBValue(vDir, aValue, aValueType, self.cache, self.version)
    def Put(self, aKey, aValue, aValueType):
        """
        """
        vDir = path.join(self.path, key)

        PutDBValue(vDir, aValue, aValueType, self.cache, self.version)
    def Delete(self, key):
        """
        """
        vDir = path.join(self.path, key)
        DeleteDBValue(vDir)
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
    def backup(self):
        return self._backup
    @backup.setter
    def backup(self, value):
        self._backup = bool(value)    
