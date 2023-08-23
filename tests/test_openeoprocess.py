from tests import basetests
import inspect
import json

from workflow import openeoprocess
from userinfo import UserInfo
from constants import constants

def testProcessKeyDefaults(test, key) :
     test.isEqual(key.id, "", "setting correct default id")
     test.isEqual(key.summary, "", "setting correct default summary")
     test.isEqual(key.description, "", "setting correct default description")     
     test.isEqual(len(key.categories), 0, "setting correct default categories")       
     test.isEqual(len(key.parameters), 0, "setting correct default parameters")     
     test.isEqual(len(key.exceptions), 0, "setting correct default exceptions")
     test.isEqual(len(key.returns), 0, "setting correct default returns") 
     test.isEqual(key.deprecated, False, "check deprecated default flag")
     test.isEqual(key.experimental, False, "check experimental default flag")     

def testProcessKeyValues(test, key) :
     test.isEqual(key.id, "test_id", "setting correct id")
     test.isEqual(key.summary, "another text", "setting correct summary")
     test.isEqual(key.process_description, "some text", "setting correct description")     
     test.isEqual(len(key.categories), 2, "setting correct categories") 
     if len(key.categories) == 2:
         test.isEqual(key.categories[0], "string", "first values of categories")
         test.isEqual(key.categories[1], "earth", "second values of categories")
     if len(key.returns) == 2 or len(key.returns) == 1:
         test.isEqual(key.returns['description'], "calculated map", "description of return") 
         test.isEqual( 'schema' in key.returns, True, "return must of contain a schema") 
     test.isEqual(len(key.exceptions) ,2, "defined exceptions")
     test.isEqual(key.deprecated, True, "check deprecated flag")
     test.isEqual(key.experimental, True, "check experimental flag")

             

class TestOpeneoprocess(basetests.BaseTest):
    def test_01_loadprocess(self):
        self.decorateFunction(__name__, inspect.stack()[0][3])
        processfile = open('./tests/test_process1.json')
        all = json.load(processfile)

        u = UserInfo(None)

        processjson = all['tests']['base_process_minimal']
        proc = basetests.testExceptionCondition3(self, True, openeoprocess.OpenEOProcess, u, processjson, 0, 'testing minimal definition and defaults') 
        if proc != None:
            self.isEqual(proc.title, "", "setting correct default title")
            self.isEqual(proc.description, "", "setting correct default description")
            self.isEqual(proc.plan, "none", "setting correct default plan")
            self.isEqual(proc.budget, constants.UNDEFNUMBER, "setting correct default budget")  
            self.isEqual(proc.log_level, "all", "setting correct default log level")
            testProcessKeyDefaults(self,proc )   

        processjson = all['tests']['base_process_full']
        proc = basetests.testExceptionCondition3(self, True, openeoprocess.OpenEOProcess, u, processjson, 0, 'testing full process def')
        if proc != None:
            self.isEqual(proc.title, "test function for testing a process ", "setting correct title")
            self.isEqual(proc.description, "Nothing usefull", "setting correct description")
            self.isEqual(proc.plan, "expensive", "setting correct plan")
            self.isEqual(proc.budget, "1000", "setting correct budget")  
            self.isEqual(proc.log_level, "who cares", "setting correct log level")  
            testProcessKeyValues(self, proc)        

        processjson = all['tests']['base_process_missing_process']
        basetests.testExceptionCondition3(self, False, openeoprocess.OpenEOProcess, u, processjson, 0, 'testing missing process')

        processjson = all['tests']['base_process_missing_process_graph']
        basetests.testExceptionCondition3(self, False, openeoprocess.OpenEOProcess, u, processjson, 0, 'testing missing process graph')

        processjson = all['tests']['base_process_minimal_missing_return_schema']
        basetests.testExceptionCondition3(self, False, openeoprocess.OpenEOProcess, u, processjson, 0, 'testing missing schema in return key')        

