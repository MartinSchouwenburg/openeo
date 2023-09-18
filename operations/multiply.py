from openeooperation import *
from operationconstants import *
from constants import constants
import math

class MultiplyOperation(OpenEoOperation):
    def __init__(self):
        self.loadOpenEoJsonDef('multiply.json')
        self.kind = constants.PDPREDEFINED

        self.a = constants.UNDEFNUMBER
        self.b = constants.UNDEFNUMBER

    def prepare(self, arguments):
        self.runnable = False

        if len(arguments) != 2:
            return  createOutput(False,"number of parameters is not correct",  constants.DTERROR)
        
        if math.isnan(arguments['a']):
            return createOutput(False, "the parameter a is not a number", constants.DTERROR)
        self.a = arguments['a']
        
        if math.isnan(arguments['b']):
            return createOutput(False, "the parameter b is not a number", constants.DTERROR)
        self.b = arguments['b']

        self.runnable = True
        return ""
              

    def run(self, job_id, processOutput, processInput):
        if self.runnable:

            put2Queue(processOutput, {'progress' : 0, 'job_id' : job_id, 'status' : 'running'})

            c = self.a * self.b

            put2Queue(processOutput,{'progress' : 100, 'job_id' : job_id, 'status' : 'finished'}) 

            return createOutput('finished', c, constants.DTNUMBER)
        
        return createOutput('error', "operation no runnable", constants.DTERROR)
        
def registerOperation():
     return MultiplyOperation()
  




