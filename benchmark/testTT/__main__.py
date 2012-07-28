import sys
sys.path.append("~/trac/lightCloud/testbench")
sys.path.append('..')
print(__path__)
import benchmark
from testTT import a

#a = PyrantTestCase()
a.test_add()
print "hi"
