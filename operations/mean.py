from openeooperation import *
from operationconstants import *
from constants import constants
from rasterdata import RasterData
from aggregatestatsBase import AggregateStatsBase

class MeanOperation(AggregateStatsBase):
    def __init__(self):
        self.loadOpenEoJsonDef('mean.json')
      
        self.kind = constants.PDPREDEFINED

    def prepare(self, arguments):
        try:
            self.base_prepare(arguments)
            self.method = 'mean'
            self.runnable = True

        except Exception as ex:
            return ""

        return ""

    def run(self, job_id, processOutput, processInput):
        return self.base_run(job_id, processOutput, processInput)

def registerOperation():
     return MeanOperation()