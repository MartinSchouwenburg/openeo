from openeooperation import *
from operationconstants import *
from constants import constants
from rasterdata import RasterData
import ilwis
import numpy

class AggregateStatsBase(OpenEoOperation):
    def base_prepare(self, arguments):
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
                self.method = 'unknown'
            if type(arguments['data']) is numpy.array: ## will this work, ftm no testable case
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
                    ilwRaster = rc.ilwisRaster
                    outputRc = ilwis.do("aggregaterasterstatistics", ilwRaster,self.method)
                    extra = self.constructExtraParams(rc, rc.temporalExtent, 0)
                    outputRasters.extend(self.setOutput([outputRc], extra))

                ##self.logEndOperation(processOutput, job_id)
                return createOutput('finished', outputRasters, constants.DTRASTER)
        
        return createOutput('error', "operation not runnable", constants.DTERROR)      