from openeooperation import *
from operationconstants import *
from constants import constants
from rasterdata import RasterData
from aggregatestatsBase import AggregateStatsBase

class MedianOperation(AggregateStatsBase):
    def __init__(self):
        self.loadOpenEoJsonDef('median.json')
      
        self.kind = constants.PDPREDEFINED

    def prepare(self, arguments):
        try:
            self.base_prepare(arguments)
            self.method = 'median'
            self.runnable = True

        except Exception as ex:
            return ""

        return ""

    def run(self, job_id, processOutput, processInput):
        return self.base_run(job_id, processOutput, processInput)

def registerOperation():
     return MedianOperation()