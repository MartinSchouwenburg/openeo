from openeooperation import *
from operationconstants import *
from constants import constants
from common import openeoip_config


class NormalizedDifference(OpenEoOperation):
    def __init__(self):
        self.loadOpenEoJsonDef('normalized_difference.json')
        
        self.kind = constants.PDPREDEFINED

    def prepare(self, arguments):
        self.runnable = True
        self.rasterSizesEqual = True
        self.inputRaster1 = arguments['x']['resolved']
        self.inputRaster2 = arguments['y']['resolved']
        if not( isinstance(self.inputRaster2, RasterData) and isinstance(self.inputRaster1, RasterData)):
            return createOutput(False, "the parameter a is not a raster", constants.DTERROR)
        
        self.createExtra(self.inputRaster1, 0) 
        return ""
              

    def run(self, job_id, processOutput, processInput):
        if self.runnable:
            self.logStartOperation(processOutput, job_id)
            outputRc = ilwis.do("mapcalc", "(@1 - @2) / (@1 + @2)", self.inputRaster1.getRaster().rasterImp(), self.inputRaster2.getRaster().rasterImp())
            outputRasters = []                
            outputRasters.extend(self.setOutput([outputRc], self.extra))
            self.logEndOperation(processOutput, job_id)
            return createOutput('finished', outputRasters, constants.DTRASTERLIST)
        message = common.notRunnableError(job_id)
        return createOutput('error', message, constants.DTERROR)
        
def registerOperation():
     return NormalizedDifference()