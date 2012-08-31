#!/usr/bin/python
#coding:utf-8

from os import path
from iDB.iDB import iDB
from iDB.helpers import IDB_SPEC_VER
import pytest
import unittest
from base_test import BaseTest

class TestIDB(BaseTest):
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
        vDB.storeInXattr == False
        vDB.Close()
        vDB.Open()
        assert vDB.storeInXattr == False


