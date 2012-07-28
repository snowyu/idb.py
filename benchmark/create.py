import sys
import os, errno
from os import makedirs, path
from idb.utils import RandomString
from idb.helpers import CreateDBString, GetDBValue

def main():
    value = RandomString()
    #value = 'F7ZKEY'
    dir = './my_testdb/'+value
    CreateDBString(dir,value)
    #GetDBValue(dir)
    #sys.stderr.write('"' + str(GetDBValue(dir)) + '"')
    #sys.stderr.write("\n")
    #mkdir_p(dir)
    #shutil.rmtree(dir)
    #sys.stderr.write("\n")
    #sys.stderr.write("add value{0}\n" % aKey)
    #sys.stderr.write(client.prefix_keys("1", 10000)[0])

main()
