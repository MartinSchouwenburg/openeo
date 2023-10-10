from openeooperation import *
from operationconstants import *
from constants import constants
from rasterdata import RasterData
from aggregatestatsBase import AggregateStatsBase

class MinOperation(AggregateStatsBase):
    def __init__(self):
        self.loadOpenEoJsonDef('min.json')
      
        self.kind = constants.PDPREDEFINED

    def prepare(self, arguments):
        try:
            self.base_prepare(arguments)
            self.method = 'min'
            self.runnable = True

        except Exception as ex:
            return ""

        return ""

    def run(self, job_id, processOutput, processInput):
        return self.base_run(job_id, processOutput, processInput)

def registerOperation():
     return MinOperation()