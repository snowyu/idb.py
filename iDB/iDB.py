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
    def __init_parms__(self,  **connection):
        kw_defaults = {path: '', cache: True}
        for key, value in kw_defaults.iteritems():
            if connection.has_key(key):
                val = connection[key]
            else:
                val = value
            setattr(self, key, val)
        self.cache = bool(self.cache)
        if self.path  ==  '':
            raise iDBError(EIDBNODIR, 'Please specify the database directory first!')

    def __init__(self, connection):
        """Open an existed database:
        iDB({'path':'/mydb', 'cache': True})
        """
        self.__init_parms__(connection)


        self.version = self.Get('.db/version')
        if self.version  == None:
            self.version = IDB_SPEC_VER

    def init(self, connection):
        """init a database:
        """
        self.__init_parms__(connection)
        ForceDirectories(self.path)
        self.version = IDB_SPEC_VER
        self.Put('.db/version', IDB_SPEC_VER, 'Float')
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
    
