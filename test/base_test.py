#!/usr/bin/python
#coding:utf-8

import pytest
import unittest
import os
from os import path
from shutil import rmtree

from iDB.utils import RandomString
from iDB.helpers import WriteFileValue, ReadFileValue, GetDBValue, RemoveFileValue, IDB_VALUE_NAME

ROOT_DIR = './mytestdb'
FIXTURE_DIR = path.join(path.realpath(__file__), 'fixtures')

def RandomKeyValue(aKeySize = 8, aValueSize = 26):
    key = RandomString(aKeySize)
    value = RandomString(aValueSize)
    return {'key': key, 'value': value}

def RandomPairs(aSize = 99):
    return [RandomKeyValue() for x in range(aSize)]

def create_pairs(aSize = 99, aCached = True):
    pairs = RandomPairs(aSize)
    for item in pairs:
        vDir = path.join(ROOT_DIR, item['key'])
        vStr = item['value']
        WriteFileValue(vDir, vStr, IDB_VALUE_NAME, aCached)
    return pairs

def delete_pairs(aPairs):
    for item in aPairs:
        vDir = path.join(ROOT_DIR, item['key'])
        RemoveFileValue(vDir)

def check_pair(aKey, aValue, aAttriubte=IDB_VALUE_NAME, wanted_result = True):
    vDir = path.join(ROOT_DIR, aKey)
    if wanted_result:
        assert path.isdir(vDir)
    else:
        check_key_removed(aKey)
    vWantedStr = aValue
    vStr = ReadFileValue(vDir, aAttriubte)
    if wanted_result:
        assert len(vStr) == 1
        vStr = vStr[0]
    if wanted_result:
        assert vStr == vWantedStr
    else:
        assert vStr == None
    vStr = ReadFileValue(vDir + RandomString(6))
    assert vStr == None
    
def check_key_removed(aKey):
    vDir = path.join(ROOT_DIR, aKey)
    assert not path.isdir(vDir)
    assert not path.isfile(vDir)

def check_pairs(pairs, wanted_result = True):
    for item in pairs:
        check_pair(item['key'], item['value'], IDB_VALUE_NAME, wanted_result)

class BaseTest(unittest.TestCase):
    def setUp(self):
        self.path = ROOT_DIR
        rmtree(ROOT_DIR,  True)
    def tearDown(self):
        rmtree(ROOT_DIR, True)

