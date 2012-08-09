import sys
import timeit
#sys.path.append('..')
#sys.path.append('../redis-py')
from shutil import rmtree

#import unittest
import datetime

from iDB import String
from iDB.utils import CreateDir
from iDB.helpers import iDBError

from benchmark import BenchmarkTestCase 


class iDBTestCase(BenchmarkTestCase):
    
    def setUp(self):
        #sys.stderr.write('connecting...\n')
        self.path = './mytestdb'
        self.backup = False
        self.xattr  = True
        CreateDir(self.path)
        #self.client.flushdb()
        
    def tearDown(self):
        rmtree(self.path)
        
    def clearDB(self):
        rmtree(self.path)
 
    def getValue(self, aKey):
        try:
            result = String.LoadFrom(path=self.path, key=aKey, xattr=self.xattr, backup=self.backup)
        except iDBError:
            result = None
        return result
    
    def addValue(self, aKey, aValue):
        #sys.stderr.write("add value{0}\n" % aKey)
        a = String(aValue, path=self.path, key=aKey, xattr=self.xattr, backup=self.backup)
        a.Save()
        return True
        #return self.client.setnx(aKey, aValue)
    
    def updateValue(self, aKey, aValue):
        a = String(path=self.path, key=aKey, xattr=self.xattr, backup=self.backup)
        if a.Exists() == True:
            a.data = aValue
            a.Save()
            return True
        else:
            return False
    
    def delKey(self, aKey):
        String.delete(self.path, aKey)
        return True
        #return self.client.delete(aKey)

#t = timeit.Timer("testRedis.a.test_add()")
#t.repeat(3, 10)


