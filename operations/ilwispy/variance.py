from openeooperation import *
from operationconstants import *
from constants import constants
from rasterdata import RasterData
from operations.ilwispy.BaseAggregatestats import BaseAggregateStats

class VarianceOperation(BaseAggregateStats):
    def __init__(self):
        self.loadOpenEoJsonDef('variance.json')
      
        self.kind = constants.PDPREDEFINED

    def prepare(self, arguments):
        try:
            self.base_prepare(arguments)
            self.method = 'variance'
            self.runnable = True

        except Exception as ex:
            return ""

        return ""

    def run(self, job_id, processOutput, processInput):
        return self.base_run(job_id, processOutput, processInput)

def registerOperation():
     return VarianceOperation()