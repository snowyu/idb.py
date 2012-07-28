import sys
#import timeit
#sys.path.append('..')
#sys.path.append('../redis-py')
import pyrant
#import unittest
#import datetime
from benchmark import BenchmarkTestCase 


class PyrantTestCase(BenchmarkTestCase):
    
    def setUp(self):
        #sys.stderr.write('connecting...\n')
        self.client = pyrant.Tyrant(host=self.Host, port=3333)
        #self.client.ensureIndex("key")
        #self.client.flushdb()
        
    def tearDown(self):
        #self.client.flushdb()
        return
        
    def clearDB(self):
        #drop the collection(table)
        self.client.vanish()
 
    def getValue(self, aKey):
        try:
           return self.client[aKey]
        except:
          return None
    def addValue(self, aKey, aValue):
        #sys.stderr.write("add value{0}\n" % aKey)
        #return 
        self.client.proto.putkeep(aKey, aValue)
        return True
    
    def updateValue(self, aKey, aValue):
        #return 
        self.client[aKey] = aValue
        return True

    def delKey(self, aKey):
        return self.client.out(aKey)
    def setIndex(self, aIndex):
        return self.client.misc('setindex', aIndex)

a = PyrantTestCase();

#t = timeit.Timer("testRedis.a.test_add()")
#t.repeat(3, 10)


