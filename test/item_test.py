#!/usr/bin/python
#coding:utf-8

import string, random
from os import path
#from shutil import rmtree

from iDB.utils import RandomString
from iDB.Item import Item, Loading
from iDB.Boolean import Boolean
from iDB.Hex import Hex
from iDB.Float import Float
from iDB.Dict import Dict
from iDB.Object import Object

from base_test import BaseTest

# self.item must be exists first.
class ItemTest(BaseTest):
    @staticmethod
    def RandomKeyValue(aKeySize = 8, aValueSize = 26):
        key = RandomString(aKeySize)
        value = RandomString(aValueSize)
        cls= random.choice(Item._ItemClasses.values())
        if issubclass(cls, int):
            value = random.randint(-99999, 99999)
        elif issubclass(cls, float):
            value = random.random()
        elif issubclass(cls, Boolean):
            value = random.choice(['true', 'false'])
        elif issubclass(cls, Dict):
            value = {'mys': RandomString(255), 'myi': random.randint(-99999, 99999)}
        else:
            cls= Item._ItemClasses['String']
        return {'key': key, 'value': value, 'cls':cls}
    @staticmethod
    def RandomPairs(aSize = 99):
        return [ItemTest.RandomKeyValue() for x in range(aSize)]

    def save_pairs(self, size=99,  ** kwargs):
        pairs = self.RandomPairs(size)
        for item in pairs:
            cls = item['cls']
            assert cls  != None
            kwargs['key'] = item['key']
            i = cls(item['value'],  ** kwargs)
            assert i != None
            item['v'] = i
            i.Save()
            assert path.isdir(path.join(i.path, i.key))
        return pairs

    def _test_load(self,  ** kwargs):
        pairs= self.save_pairs(** kwargs)
        for item in pairs:
            cls = item['cls']
            i = cls.LoadFrom(key=item['key'], loadOnDemand=False,  ** kwargs)
            vPath = path.join(i.path, i.key)
            assert path.isdir(vPath)
            assert type(i) == type(item['v'])
            if isinstance(i, float):
                assert i-item['v']  <= 0.000000001
            else:
                assert i == item['v']
            i.Load()
            if isinstance(i, float):
                assert i-item['v']  <= 0.000000001
            else:
                assert i == item['v']
            if type(i) == Dict:
                i = cls.LoadFrom(key=item['key'], loadOnDemand=True,  ** kwargs)
                assert type(i) == type(item['v'])
                for x, y in i.iteritems():
                    assert item['v'].has_key(x)
                    assert isinstance(y, Loading)
                i.Load()
                for x, y in i.iteritems():
                    assert item['v'].has_key(x)
                    assert isinstance(y, Loading)
    def test_load_xattr(self):
        self._test_load(path=self.path, storeInFile=False, storeInXattr=True)
 
    def test_load_file(self):
        self._test_load(path=self.path, storeInFile=True, storeInXattr=False)
    def test_load(self):
        self._test_load(path=self.path, storeInFile=True, storeInXattr=True)
    def test_save(self):
        data = {'hi':'word', 'myke':'fghhfssd'}
        a=Dict(data, path=self.path, key='myd');
        a.Save()
        a=Dict.LoadFrom(path=self.path, key='myd', loadOnDemand=True)
        a.Save()
        assert data == a
    def test_save_obj(self):
        data = {'hi':'word', 'myke':'fghhfssd'}
        a=Dict(data, path=self.path, key='myd');
        a.Save()
        a=Object.LoadFrom(path=self.path, key='myd', loadOnDemand=True)
        a.key = 'myo'
        a.Save()
        assert data == a

