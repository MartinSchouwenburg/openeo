from openeooperation import *
from operationconstants import *
from constants import constants
from workflow import processGraph
from globals import getOperation

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
                outputInfo = process.run(job_id, processOutput, processInput)
            else:
                return createOutput('finished', self.reducer['resolved'], constants.DTRASTER) 
        return createOutput('error', "operation no runnable", constants.DTERROR)
        
def registerOperation():
     return ReduceDimensionsOperation()
  




