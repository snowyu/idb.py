#!/usr/bin/python
#coding:utf-8

import idb.helpers
import pytest
import unittest
import base_test

from os import path
from idb.utils import RandomString, GetDirCount
from shutil import rmtree
from base_test import BaseTest, ROOT_DIR

class TestIDBHelpers(BaseTest):
    def test_CreateDBString(self):
        pairs = base_test.create_pairs(199)
        assert GetDirCount(ROOT_DIR) == len(pairs)
        base_test.check_pairs(pairs)
    def test_CreateDBStringNoCahce(self):
        pairs = base_test.create_pairs(199, False)
        assert GetDirCount(ROOT_DIR) == len(pairs)
        base_test.check_pairs(pairs)

