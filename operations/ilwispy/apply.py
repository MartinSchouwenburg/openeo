from openeooperation import *
from operationconstants import *
from constants import constants
from common import openeoip_config
from workflow import processGraph
from globals import getOperation


class ApplyOperation(OpenEoOperation):
    def __init__(self):
        self.loadOpenEoJsonDef('apply.json')
        
        self.kind = constants.PDPREDEFINED

    def prepare(self, arguments):
        self.runnable = True
        self.data = arguments['data']['resolved']
        self.apply = arguments['process']['base']

        return ""
              

    def run(self, job_id, processOutput, processInput):
        if self.runnable:
            self.logStartOperation(processOutput, job_id)
            if self.apply != None:
                pgraph = self.apply['process_graph']
                process = processGraph.ProcessGraph(pgraph, self.data, getOperation)
                return process.run(job_id, processOutput, processInput)
        
        return createOutput('error', "operation no runnable", constants.DTERROR)
        
def registerOperation():
     return ApplyOperation()