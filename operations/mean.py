from openeooperation import *
from operationconstants import *
from constants import constants
from rasterdata import RasterData
import ilwis

class MeanOperation(OpenEoOperation):
    def __init__(self):
        self.loadOpenEoJsonDef('mean.json')
      
        self.kind = constants.PDPREDEFINED
    

    def prepare(self, arguments):
        try:
            self.runnable = False 
            if type(arguments['data'][0]) is RasterData:
                self.rasters = arguments['data']
                if len(self.rasters) == 0:
                    return 'invalid input. Number of rasters is 0'

                for rc in self.rasters:
                    if not rc:
                        return 'invalid input. rasters are not valid'
                    if rc.ilwisRaster.datadef().domain().ilwisType() != ilwis.it.NUMERICDOMAIN:
                        return 'invalid datatype in raster. Must be numeric'
    
                self.rasterSizesEqual = self.checkSpatialDimensions(self.rasters)  
            
            self.runnable = True
        except Exception as ex:
            return ""

        return ""

    def run(self, job_id, processOutput, processInput):
        if self.runnable:
            if hasattr(self, 'rasters'):
                rasters = []
                for rc in self.rasters:
                    ilwRaster = rc.ilwisRaster
                    outputRc = ilwis.do("aggregaterasterstatistics", ilwRaster, "mean")
                    rasters.append(outputRc)

                extra = self.constructExtraParams(self.rasters[0], self.rasters[0].temporalExtent, 0)
                outputRasters =  self.setOutput(rasters, extra)
        
                return createOutput('finished', outputRasters, constants.DTRASTER)
        
        return createOutput('error', "operation not runnable", constants.DTERROR)

                  
        
def registerOperation():
     return MeanOperation()