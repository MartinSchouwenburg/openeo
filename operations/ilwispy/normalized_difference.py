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
        self.inputRast1 = arguments['x']['resolved']
        self.inoutRaster2 = arguments['y']['resolved']
        self.createExtra(self.inputRast1, 0) 
        return ""
              

    def run(self, job_id, processOutput, processInput):
        if self.runnable:
            outputRc = ilwis.do("mapcalc", "(@1 - @2) / (@1 + @2)", self.inputRast1.getRaster().rasterImp(), self.inoutRaster2.getRaster().rasterImp())
            outputRasters = []                
            outputRasters.extend(self.setOutput([outputRc], self.extra))
            return createOutput('finished', outputRasters, constants.DTRASTERLIST)
        
        return createOutput('error', "operation no runnable", constants.DTERROR)
        
def registerOperation():
     return NormalizedDifference()