from openeooperation import *
from operationconstants import *
from constants import constants
from common import openeoip_config


class LinearScaleRangeOperation(OpenEoOperation):
    def __init__(self):
        self.loadOpenEoJsonDef('linear_scale_range.json')
        
        self.kind = constants.PDPREDEFINED

    def prepare(self, arguments):
        self.runnable = True
        self.rasterSizesEqual = True
        self.inpMax = arguments['inputMax']['resolved']
        self.inpMin = arguments['inputMin']['resolved']
        self.outMax = arguments['outputMax']['resolved']
        self.outMin = arguments['outputMin']['resolved']
        last_key = list(arguments)[-1]
        raster = arguments[last_key]['resolved']
        if not isinstance(raster, RasterData):
            return 'invalid input. rasters are not valid'

        if raster.getRaster().dataType() != ilwis.it.NUMERICDOMAIN:
            return 'invalid datatype in raster. Must be numeric'
        self.inputRaster = raster.getRaster().rasterImp()
        self.createExtra(raster, 0) 
        return ""
              

    def run(self, job_id, processOutput, processInput):
        if self.runnable:
            self.logStartOperation(processOutput, job_id)

            outputRc = ilwis.do("linearstretch", self.inputRaster,self.inpMin, self.inpMax, self.outMin, self.outMax)
            outputRasters = []                
            outputRasters.extend(self.setOutput([outputRc], self.extra))
            return createOutput('finished', outputRasters, constants.DTRASTERLIST)
        
        return createOutput('error', "operation no runnable", constants.DTERROR)
        
def registerOperation():
     return LinearScaleRangeOperation()