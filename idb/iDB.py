#!/usr/bin/python
#coding:utf-8

import os
import sys, errno
import glob
from os import path

from utils import CreateDir
from helpers import IDB_SPEC_VER, GetDBValue, iDBError
from helpers import EIDBNODIR

class iValue(object):
    def __init__(self, aType, aValue):
        self.ValueType = aType
        self.value = aValue

class iDB(object):
    """
    """
    def __init__(self, aDBRootDir):
        if aDBRootDir  ==  '':
            raise iDBError(EIDBNODIR, 'Please specify the database directory first!')
        else:
            aDBRootDir = aDBRootDir
            CreateDir(aDBRootDir)
            self.root = aDBRootDir
            self.version = self.Get('.db/version')
            if self.version  == None:
                self.version = IDB_SPEC_VER

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
        """
        """
    def Delete(self, key):
        """
        """
    
