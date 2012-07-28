import sys
import timeit
#sys.path.append('..')
#sys.path.append('../redis-py')
import redis

#import unittest
import datetime
from benchmark import BenchmarkTestCase 


class RedisTestCase(BenchmarkTestCase):
    
    def setUp(self):
        #sys.stderr.write('connecting...\n')
        self.client = redis.Redis(host='localhost', port=3333, db=0)
        #self.client.flushdb()
        
    def tearDown(self):
        self.client.flushdb()
        
    def clearDB(self):
        self.client.flushdb()
 
    def getValue(self, aKey):
        return self.client.get(aKey)
    
    def addValue(self, aKey, aValue):
        #sys.stderr.write("add value{0}\n" % aKey)
        return self.client.setnx(aKey, aValue)
    
    def updateValue(self, aKey, aValue):
        if self.client.exists(aKey) == True:
          return self.client.set(aKey, aValue)
        else:
          return False
    
    def delKey(self, aKey):
        return self.client.delete(aKey)

#t = timeit.Timer("testRedis.a.test_add()")
#t.repeat(3, 10)


