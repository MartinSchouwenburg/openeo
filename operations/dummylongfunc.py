from openeooperation import *
from operations.operationconstants import *
from constants.constants import *
import time


class DummyLongFunc(OpenEoOperation):
    def __init__(self):

        self.name = 'dummylongfunc'
        self.description = 'dummy function that does nothing but run for some time. needed for testing'
        self.summary = 'dummy needed fror testing'
        self.categories = ['test']
        self.exceptions['DummyError'] = { 'message': 'I am dumb'}

        self.addInputParameter('a', 'why not', OPERATION_SCHEMA_NUMBER)

        self.addOutputParameter('to complete things',OPERATION_SCHEMA_NUMBER)
        self.kind = PDUSERDEFINED

        self.a = UNDEFNUMBER

    def prepare(self, arguments):
            self.runnable = True

            self.a = arguments['a']

            return ""

    def run(self, job_id, processOutput):
            if self.runnable:
                lasttime = time.time()
                for i in range(self.a):
                    time.sleep(1)
                    currenttime = time.time()
                    if currenttime - lasttime > 5:
                        f = float(i/self.a)
                        p = int(100 * f)
                        processOutput.put({'progress' : p, 'job_id' : job_id, 'status' : 'running'})     
                        lasttime = currenttime
                         
                processOutput.put({'progress' : 100, 'job_id' : job_id, 'status' : 'finished'})   
                return createOutput('finished', 23, DTNUMBER)
            
            return createOutput('error', "operation not runnable", DTERROR)

def registerOperation():
     return DummyLongFunc()