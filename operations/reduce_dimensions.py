from openeooperation import *
from operationconstants import *
from constants import constants
from workflow import workflow
from globals import getOperation

class ReduceDimensionsOperation(OpenEoOperation):
    def __init__(self):
        self.loadOpenEoJsonDef('reduce_dimension.json')
        
        self.kind = constants.PDPREDEFINED

    def prepare(self, arguments):
        self.runnable = False
        g = arguments['reducer']['process_graph']
        args = self.setArguments(g, {'data' : arguments['data']})
        self.reducerGraph = workflow.Workflow(args, getOperation)
        self.runnable = True
        return ""
              

    def run(self, job_id, processOutput, processInput):
        if self.runnable:
            outputInfo = self.reducerGraph.run(job_id, processOutput, processInput)
            if 'value' in outputInfo:
                return createOutput('finished', outputInfo['value'], constants.DTRASTER)
        
        return createOutput('error', "operation no runnable", constants.DTERROR)
        
def registerOperation():
     return ReduceDimensionsOperation()
  




