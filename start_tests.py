import unittest
from  tests import configglobals
import os
import sys
configglobals.errorCount = 0

#time.sleep(10)

pp = os.getcwd()
sys.path.append(pp + '/workflow')
sys.path.append(pp + '/constants')
sys.path.append(pp + '/operations')
sys.path.append(pp + '/tests')
sys.path.append(pp)

loader = unittest.TestLoader()

cls = configglobals.ErrorManager()
cls.init()

tests = loader.discover('./tests','test_*.py')
testRunner = unittest.runner.TextTestRunner()
testRunner.run(tests)

tcount = cls.testCount()
ecount = cls.errorCount()
elist = cls.errorList()

print("\nnumber of tests : " + tcount)
print("number of fails in tests : " + ecount)
print("error list : " + elist)

