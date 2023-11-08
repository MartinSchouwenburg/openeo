from openeooperation import *
from operationconstants import *
from constants import constants
from rasterdata import RasterData
import ilwis
import numpy

class BaseAggregateData(OpenEoOperation):
    def base_prepareRaster(self, arguments):
        try:
            self.runnable = False 
            inpData = arguments['data']['resolved']
            if len(inpData) == 0:
                return 'invalid input. Number of rasters is 0'            
            if isinstance(inpData[0], RasterData):
                self.rasters = inpData

                for rc in self.rasters:
                    if not rc:
                        return 'invalid input. rasters are not valid'
                    if rc.getRaster().dataType() != ilwis.it.NUMERICDOMAIN:
                        return 'invalid datatype in raster. Must be numeric'
    
                self.rasterSizesEqual = self.checkSpatialDimensions(self.rasters)  
                self.method = 'unknown'
            elif type(arguments['data']) is numpy.array: ## will this work, ftm no testable case
                self.array = arguments['data']
                self.aggFunc = numpy.mean
            
        except Exception as ex:
            return ""

        return ""
      
    def base_run(self, job_id, processOutput, processInput):
        if self.runnable:
            self.logStartOperation(processOutput, job_id)
            if hasattr(self, 'rasters'):
                outputRasters = []
                for rc in self.rasters:
                    raster = rc.getRaster().rasterImp()
                    outputRc = ilwis.do("aggregaterasterstatistics", raster,self.method)
                    extra = self.constructExtraParams(rc, rc.temporalExtent, 0)
                    outputRasters.extend(self.setOutput([outputRc], extra))

                ##self.logEndOperation(processOutput, job_id)
                return createOutput('finished', outputRasters, constants.DTRASTER)
        
        return createOutput('error', "operation not runnable", constants.DTERROR)      