from openeooperation import *
from operations.operationconstants import *
from constants.constants import *
from processmanager import globalProcessManager
import time
import random
from datetime import datetime


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
                logCount = 0
                lasttime = time.time()
                for i in range(self.a):
                    time.sleep(1)
                    currenttime = time.time()
                    r = random.random() * 100
                    if r > 95.0:
                         globalProcessManager.addLog4job(job_id, logCount, 'warning', 'dummy message ' + str(r))
                         processOutput.put({'type' : 'logginevent', 'job_id': job_id, 'id' : logCount, 'level' : 'info', 'message' : 'dummy ' + str(r), 'time' : str(datetime.now())})
                         logCount = logCount + 1

                    if currenttime - lasttime > 5:
                        f = float(i/self.a)
                        p = int(100 * f)
                        processOutput.put({'type': 'progressevent','progress' : p, 'job_id' : job_id, 'status' : 'running'})     
                        lasttime = currenttime
                                            
                         
                processOutput.put({'type': 'progressevent', 'progress' : 100, 'job_id' : job_id, 'status' : 'finished'})   
                return createOutput('finished', 23, DTNUMBER)
            
            return createOutput('error', "operation not runnable", DTERROR)

def registerOperation():
     return DummyLongFunc()