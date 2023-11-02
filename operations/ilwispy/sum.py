from openeooperation import *
from operationconstants import *
from constants import constants
from rasterdata import RasterData
from operations.ilwispy.BaseAggregatestats import BaseAggregateStats

class SumOperation(BaseAggregateStats):
    def __init__(self):
        self.loadOpenEoJsonDef('sum.json')
      
        self.kind = constants.PDPREDEFINED

    def prepare(self, arguments):
        try:
            self.base_prepare(arguments)
            self.method = 'sum'
            self.runnable = True

        except Exception as ex:
            return ""

        return ""

    def run(self, job_id, processOutput, processInput):
        return self.base_run(job_id, processOutput, processInput)

def registerOperation():
     return SumOperation()