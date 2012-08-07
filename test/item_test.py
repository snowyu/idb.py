#!/usr/bin/python
#coding:utf-8

import string, random

from iDB.utils import RandomString
from iDB.Item import Item
from iDB.Boolean import Boolean
from iDB.Hex import Hex

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
        elif issubclass(cls, Boolean):
            value = random.choice(['true', 'false'])
        else:
            cls= Item._ItemClasses['String']
        return {'key': key, 'value': value, 'cls':cls}
    @staticmethod
    def RandomPairs(aSize = 99):
        return [ItemTest.RandomKeyValue() for x in range(aSize)]

    def save_pairs(self, size=99):
        pairs = self.RandomPairs(size)
        for item in pairs:
            cls = item['cls']
            i = cls(item['value'], path=self.path, key=item['key'])
            item['v'] = i
            i.Save()
        return pairs

    def test_load(self):
        pairs= self.save_pairs()
        for item in pairs:
            cls = item['cls']
            i = cls.LoadFrom(path=self.path, key=item['key'])
            assert type(i) == type(item['v'])
            assert i  == item['v']
