import os

class ErrorManager:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ErrorManager, cls).__new__(cls)
        return cls.instance
    
    def init(self):
        os.environ["OPENEO_TEST_COUNT"] = "0"
        os.environ["OPENEO_ERROR_COUNT"] = "0"
        os.environ["OPENEO_ERROR_LIST"] = ""
  
    def incTestCount(self):
        c = int(os.environ["OPENEO_TEST_COUNT"]) 
        c +=1
        os.environ["OPENEO_TEST_COUNT"] = str(c)

    def testCount(self):
        return os.environ["OPENEO_TEST_COUNT"]

    def errorCount(self):
        return os.environ["OPENEO_ERROR_COUNT"]

    def errorList(self):
        return os.environ["OPENEO_ERROR_LIST"]

    def addErrorNumber(self, num):
        c = int(os.environ["OPENEO_ERROR_COUNT"]) 
        c +=1
        os.environ["OPENEO_ERROR_COUNT"] = str(c)

        en = os.environ["OPENEO_ERROR_LIST"]
        en += ":" + str(num)
        os.environ["OPENEO_ERROR_LIST"] = en

        