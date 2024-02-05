from openeooperation import *
from operationconstants import *
from constants import constants
from workflow import processGraph
from globals import getOperation
import logging
import common

class ReduceDimensionsOperation(OpenEoOperation):
    def __init__(self):
        self.loadOpenEoJsonDef('reduce_dimension.json')
        
        self.kind = constants.PDPREDEFINED

    def prepare(self, arguments):
        self.runnable = False
        self.reducer= arguments['reducer']
        self.data = arguments['data']
        self.runnable = True
        return ""
              

    def run(self, job_id, processOutput, processInput):
        if self.runnable:
            self.logStartOperation(processOutput, job_id)
            if self.reducer['resolved'] == None:
                pgraph = self.reducer['process_graph']
                args = self.data['base']
                process = processGraph.ProcessGraph(pgraph, args, getOperation)
                output =  process.run(job_id, processOutput, processInput)
                self.logEndOperation(processOutput, job_id)
                return output
            else:
                self.logEndOperation(processOutput, job_id)
                return createOutput('finished', self.reducer['resolved'], constants.DTRASTER)
        message = common.notRunnableError(job_id)           
        return createOutput('error', message, constants.DTERROR)
        
def registerOperation():
     return ReduceDimensionsOperation()
  




