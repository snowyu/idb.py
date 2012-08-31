#!/usr/bin/python
#coding:utf-8

import string, random
from os import path
from iDB.iDB import iDB
from iDB.Dict import Dict
from iDB.helpers import IDB_SPEC_VER, ReadValueFromFile
from iDB.utils import IsXattrExists, GetXattr, RandomString
import pytest
import unittest
from base_test import BaseTest

class TestIDB(BaseTest):
    @staticmethod
    def RandomKeyValue(aKeyPrefix='', aKeySize = 8, aValueSize = 26):
        key = aKeyPrefix + RandomString(aKeySize)
        value = RandomString(aValueSize)
        cls= random.choice([int, int, float, bool, bool, str, str, dict])
        if issubclass(cls, int):
            value = random.randint(-99999, 99999)
        elif issubclass(cls, float):
            value = random.random()
        elif issubclass(cls, bool):
            value = random.choice([True, False])
        elif issubclass(cls, dict):
            value = {'mys': RandomString(255), 'myi': random.randint(-99999, 99999)}
        else:
            cls= str
        return {'key': key, 'value': value, 'cls':cls}
    @staticmethod
    def RandomPairs(aKeyPrefix='', aSize = 99):
        return [TestIDB.RandomKeyValue(aKeyPrefix) for x in range(aSize)]

    def setUp(self):
        super(TestIDB, self).setUp()
        self.FDB = iDB(path=self.path)
    def test_open(self):
        vDB = self.FDB
        vDB.Open()
        assert vDB.opened
        vMetaPath = path.join(self.path, '.db')
        assert path.isdir(vMetaPath)
        assert vDB.version == IDB_SPEC_VER
        assert vDB.storeInFile == True
        assert vDB.storeInXattr == True
        assert vDB.loadOnDemand == True
        vDB.storeInXattr = False
        vDB.loadOnDemand = False
        vDB.Close()
        assert vDB.Get('.db') == None
        assert vDB.Put('mykeey',  'ddddas') == None
        assert not path.isdir(path.join(self.path, 'mykeey'))
        assert vDB.Delete('.db') == None
        assert path.isdir(vMetaPath)
        vDB.Open()
        assert isinstance(vDB.Get('.db'), Dict)
        assert vDB.storeInXattr == False
        assert vDB.loadOnDemand == False
        vDB.Close()
    def test_set_get_file_xattr(self):
        vDB = self.FDB
        vDB.loadOnDemand = True
        vDB.storeInFile = True
        vDB.storeInXattr = True
        vDB.Open()
        vDB.Put('mykeey',  'ddddas')
        vPath = path.join(self.path, 'mykeey')
        assert path.isfile(path.join(vPath, '.value'))
        assert IsXattrExists(vPath, '.value')
        assert GetXattr(vPath, '.value') == 'ddddas'
        assert ReadValueFromFile(vPath) == ['ddddas']
        assert vDB.Get('mykeey') == 'ddddas'
        vDB.Close()
    def test_set_get_file(self):
        vDB = self.FDB
        vDB.loadOnDemand = True
        vDB.storeInFile = True
        vDB.storeInXattr = False
        vDB.Open()
        vDB.Put('mykeey',  'ddddas')
        assert path.isfile(path.join(self.path, 'mykeey', '.value'))
        assert vDB.Get('mykeey') == 'ddddas'
        vDB.Close()
    def do_get(self, db, key, expect_result):
        db.loadOnDemand = False
        result = db.Get(key)
        if isinstance(result, float):
            assert result-expect_result  <= 0.000000001
        else:
            assert result == expect_result 

    def test_set_get_xattr(self):
        vDB = self.FDB
        vDB.loadOnDemand = True
        vDB.storeInFile = False
        vDB.storeInXattr = True
        vDB.Open()
        vDB.Put('mykeey',  'ddddas')
        assert path.isdir(path.join(self.path, 'mykeey'))
        assert not path.exists(path.join(self.path, 'mykeey', '.value'))
        assert vDB.Get('mykeey') == 'ddddas'
        vDB.Close()
    def test_delete(self):
        vDB = self.FDB
        vDB.Open()
        vDB.Put('mykeey',  'ddddas')
        assert path.isdir(path.join(self.path, 'mykeey'))
        vDB.Delete('mykeey')
        assert not path.isdir(path.join(self.path, 'mykeey'))
        vDB.Close()
    def test_WildcardSearch(self):
        vDB = self.FDB
        vDB.Open()
        assert vDB.opened
        pairs = self.RandomPairs('my', 150)
        expect_keys = []
        for i in pairs:
            expect_keys.append(i['key'])
        for i in pairs:
            assert vDB.Put(i['key'], i['value']) == True
            self.do_get(vDB, i['key'], i['value'])
        result = vDB.WildcardSearch('my*')
        keys = result['keys']
        for i in expect_keys:
            assert keys.count(i) == 1





