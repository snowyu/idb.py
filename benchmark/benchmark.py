#import unittest
import datetime
import sys
#import timeit
import random

BenchmarkSeed = 12334
#random.seed(BenchmarkSeed)

def RandomString(aLength, aPattern = None):
    if aPattern is None:
        aPattern = u'1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLOMNOPQRSTUVWXYZ,&<>;?#:@~[]{}-=+()*^%$!'
    vResult  = u''
    for i in range(aLength):
        vResult = vResult + random.choice(aPattern)
    return vResult

#unittest.TestCase
class BenchmarkTestCase():
    MaxNumber = 10000
    Host = '192.168.18.16'
    #Host = '127.0.0.1'
    def __init__(self):
        self.setUp()
    def setUp(self):
        return None        
    def tearDown(self):
        return None

    def addKeysToGet(self):
        random.seed(BenchmarkSeed)
        for i in range(1000):
            self.test_add()
        random.seed()
    def testKeysToGet(self):
        random.seed(BenchmarkSeed)
        for i in range(1000):
            aKey   = self.getKeyString()
            #aValue = '{"'+ self.getKeyString() + '":"'+ RandomString(512)+'"}'
            aValue = 'column1\0'+RandomString(128)+'\0column2\0'+RandomString(128)+'\0column3\0'+RandomString(128)
            if self.getValue(aKey) == aValue:
                sys.stderr.write("get key value is not match.\n")
                exit(1)
        random.seed()
    def getKeyString(self):
        return RandomString(128, u'1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLOMNOPQRSTUVWXYZ');
    # these methods need override:
    def clearDB(self):
        return None
    def getValue(self, aKey):
        return None
    def addValue(self, aKey, aValue):
        return False
    def delKey(self, aKey):
        return False
    def delIndex(self, aIndex):
        return False
    def updateValue(self, aKey, aValue):
        return False
    def setIndex(self, aIndex):
        return False
    #get the current db record count.
    def getCount(self):
        return -1

    def test_add(self):
        aKey   = self.getKeyString()
        #aValue = '{"'+ self.getKeyString() + '":"'+ RandomString(4098)+'"}'
        aValue = 'column1\0'+RandomString(128)+'\0column2\0'+RandomString(128)+'\0column3\0'+RandomString(128)
        if self.addValue(aKey, aValue) != True:
          sys.stderr.write('can not add the value!\n\n')
          sys.exit(1)
          return
        #self.assertEquals(self.addValue(aKey, aValue), true)

    def test_get(self):
        self.getValue(self.getKeyString())
        #if self.getValue(self.getKeyString()) == None:
            #print("can not get value now.")

        #lastCount = self.getCount()
        #lastTime  = time.clock()
        #for i in range(MaxNumber):
        #self.failIf(self.getValue(aKey) == None)
        #lastTime = time.clock() - lastTime
        #lastCount += self.getCount()
        #self.assertEquals(self.getCount(), lastCount)

