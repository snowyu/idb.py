import sys
#import timeit
#sys.path.append('..')
#sys.path.append('../redis-py')
import pymongo

#import unittest
#import datetime
from benchmark import BenchmarkTestCase 


class MongoTestCase(BenchmarkTestCase):
    
    def setUp(self):
        #sys.stderr.write('connecting...\n')
        self.connection = pymongo.Connection('localhost', 3333)
        self.db = self.connection['test']
        self.client = self.db['table']
        #self.client.ensureIndex("key")
        #self.client.flushdb()
        
    def tearDown(self):
        #self.client.flushdb()
        return
        
    def clearDB(self):
        #drop the collection(table)
        self.client.drop()
 
    def getValue(self, aKey):
        return self.client.find_one({"_id":aKey})
    
    def addValue(self, aKey, aValue):
        #sys.stderr.write("add value{0}\n" % aKey)
        return self.client.insert( {"_id":aKey, "value":aValue}) != None

    def updateValue(self, aKey, aValue):
        return self.client.update({"_id":aKey}, {"_id": aKey, "value": aValue})

    def delKey(self, aKey):
        return self.client.remove({"_id":aKey})

    def setIndex(self, aIndex):
        return self.client.ensureIndex(aIndex)

a = MongoTestCase();

#t = timeit.Timer("testRedis.a.test_add()")
#t.repeat(3, 10)


