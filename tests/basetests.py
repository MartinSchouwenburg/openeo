import unittest
import configglobals


def testExceptionCondition6(p, expected,func, parm1, parm2, parm3, parm4, parm5, parm6, message):
      try:
           obj = func(parm1, parm2, parm3, parm4, parm5, parm6)
           p.isTrue(expected, message)
           return obj
      except Exception as ex:
           p.isTrue(not expected, message)

def testExceptionCondition5(p, expected, func, parm1, parm2, parm3, parm4, parm5, message):
      try:
           obj = func(parm1, parm2, parm3, parm4, parm5)
           p.isTrue(True, expected)
           return obj
      except Exception as ex:
           p.isTrue(True, not expected)
           return False

def testExceptionCondition4(p, expected, func, parm1, parm2, parm3, parm4, message):
      try:
           obj = func(parm1, parm2, parm3, parm4)
           p.isTrue(expected, message)
           return obj
      except Exception as ex:
           p.isTrue(not expected, message)
           return None

def testExceptionCondition3(p, expected, func, parm1, parm2, parm3, message):
      try:
           obj = func(parm1, parm2, parm3)
           p.isTrue(expected, message)
           return obj
      except Exception as ex:
           p.isTrue(not expected, message)
           return None

def testExceptionCondition2(p, expected, func, parm1, parm2, message):
      try:
           obj = func(parm1, parm2)
           p.isTrue(expected, message)
           return obj
      except Exception as ex:
           p.isTrue(not expected, message)

def testExceptionCondition1(p, expected, func, parm1, message):
      try:
           p = configglobals.ErrorManager()
           obj = func(parm1)
           p.isTrue(expected, message)
           return obj
      except Exception as ex:
           p.isTrue(not expected, message)
           return None           

class BaseTest(unittest.TestCase):
    
    def decorateFunction(self, mod, fn) :
        self.decoration = mod + " ==> " + fn 
        print("\n" + self.decoration + "\n")


    def isEqual(self, str1, str2, msg):
        cls = configglobals.ErrorManager()
        cls.incTestCount()
        result = 'SUCCESS'
        if (str1 != str2):
           cls.addErrorNumber(cls.testCount())
           result = 'FAIL'

        print(f'{cls.testCount():5} {msg:65}  {result}')

    def isAlmostEqualNum(self, num1, num2, delta, msg) :
        cls = configglobals.ErrorManager()
        cls.incTestCount()
        result = 'SUCCESS'
        if (abs(num1 - num2) > delta):
           cls.addErrorNumber(cls.testCount())
           result = 'FAIL'

        print(f'{cls.testCount():5} {msg:65}  {result}')

 
    def isTrue(self, b, msg):
        cls = configglobals.ErrorManager()
        cls.incTestCount() 
        result = 'FAIL'
        if (b):
           result = 'SUCCESS'
        else:
            cls.addErrorNumber(cls.testCount())         
        print(f'{cls.testCount():5} {msg:65}  {result}')

    def isFalse(self, b, msg):
        cls = configglobals.ErrorManager()
        cls.incTestCount() 
        result = 'SUCCESS'
        if (b):
            cls.addErrorNumber(cls.testCount())  
            result = 'FAIL'
        print(f'{cls.testCount():5} {msg:65}  {result}')
                     

   


    


           

