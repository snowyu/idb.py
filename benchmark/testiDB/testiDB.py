import sys
import timeit
#sys.path.append('..')
#sys.path.append('../redis-py')
from shutil import rmtree
from os import path

#import unittest
import datetime

from iDB import String
from iDB import iDB
from iDB.utils import ForceDirectories
from iDB.helpers import iDBError

from benchmark import BenchmarkTestCase 


class iDBTestCase(BenchmarkTestCase):
    
    def setUp(self):
        #sys.stderr.write('connecting...\n')
        self.path = path.expanduser('~/mytestdb')
        self.backup = False
        self.xattr  = True
        self.db   = iDB(path=self.path, storeInFile=self.backup, storeInXattr=self.xattr)
        self.db.Open()
        #ForceDirectories(self.path)
        #self.client.flushdb()
        
    def tearDown(self):
        rmtree(self.path)
        
    def clearDB(self):
        rmtree(self.path)
 
    def getValue(self, aKey):
        try:
            #result = String.LoadFrom(path=self.path, key=aKey, storeInXattr=self.xattr, storeInFile=self.backup)
            result = self.db.Get(aKey)
        except iDBError:
            result = None
        return result
    
    def addValue(self, aKey, aValue):
        #sys.stderr.write("add value{0}\n" % aKey)
        #a = String(aValue, path=self.path, key=aKey, storeInXattr=self.xattr, storeInFile=self.backup)
        #a.Save()
        self.db.Put(aKey, aValue)
        return True
        #return self.client.setnx(aKey, aValue)
    
    def updateValue(self, aKey, aValue):
        a = String(path=self.path, key=aKey, storeInXattr=self.xattr, storeInFile=self.backup)
        if a.Exists() == True:
            a.data = aValue
            a.Save()
            return True
        else:
            return False
    
    def delKey(self, aKey):
        #String.delete(self.path, aKey)
        self.db.Delete(aKey)
        return True
        #return self.client.delete(aKey)

#t = timeit.Timer("testRedis.a.test_add()")
#t.repeat(3, 10)


