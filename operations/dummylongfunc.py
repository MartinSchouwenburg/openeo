from openeooperation import *
from operations.operationconstants import *
from constants.constants import *
from processmanager import globalProcessManager
import time
import random
import datetime
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

    def estimate(self, estimationValues, argumentValues):
        outputInfo = { 'outputdimensions' : [3,3], 'outputtype' : DTRASTER, 'outputsubtype' : DTNUMBER}
        outputcost = { 'cost' : 20, 'duration' : 100, 'size' : 34, 'expires' : datetime.datetime(2025,1,1)}

        return (True, outputInfo, outputcost)
         
    def prepare(self, arguments):
            self.runnable = True

            self.a = arguments['a']

            return ""

    def run(self, job_id, processOutput, processInput):
            if self.runnable:
                logCount = 0
                lasttime = time.time()
                self.startListener(processInput)

                for i in range(self.a):
                    time.sleep(1)
                    currenttime = time.time()
                    r = random.random() * 100
                    if r > 95.0:
                        globalProcessManager.addLog4job(job_id, logCount, 'warning', 'dummy message ' + str(r))
                        timenow = str(datetime.now())
                        processOutput.put({'type' : 'logginevent', 'job_id': job_id, 'id' : logCount, 'level' : 'info', 'message' : 'dummy ' + str(r), 'timestamp' : timenow})
                        logCount = logCount + 1

                    if currenttime - lasttime > 5:
                        p = int(100 * float(i/self.a))
                        messageProgress(processOutput, job_id, p)
                            
                        lasttime = currenttime

                    if self.stopped == True:
                        break 
                        
                                            
                status = STATUSFINISHED
                if self.stopped == True:
                    status = STATUSSTOPPED

                processOutput.put({'type': 'progressevent', 'progress' : 100, 'job_id' : job_id, 'status' : status}) 
                  
                return createOutput(status, 23, DTNUMBER)
            
            return createOutput('error', "operation not runnable", DTERROR)

def registerOperation():
     return DummyLongFunc()