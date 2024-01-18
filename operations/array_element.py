from openeooperation import *
from operationconstants import *
from constants import constants
from rasterdata import *
from common import getRasterDataSets
import ilwis
from pathlib import Path

class ArrayElementOperation(OpenEoOperation):
    def __init__(self):
        self.loadOpenEoJsonDef('array_element.json')
        
      
        self.kind = constants.PDPREDEFINED

    def prepare(self, arguments):
        try:
            self.runnable = False
            self.inputRasters = arguments['data']['resolved'] 
            if self.inputRasters == None:
                return "NotFound"

            if 'index' in arguments:
                self.bandIndex = arguments['index']['resolved']  
                if len(self.inputRasters) <= self.bandIndex:
                    return "Number of raster bands doesnt match given index"
            if 'label' in arguments:
                self.bandIndex = -1
                for idx in range(len(self.inputRasters)):
                    for item in self.inputRasters[idx].bands:
                        if item['name'] == arguments['label']['resolved']:
                            self.bandIndex = idx
                            break
                if self.bandIndex == -1:
                    return "Label can't be found in the rasters"
            self.runnable = True
 
        except Exception as ex:
            return ""

        return ""
   
    def run(self, job_id, processOutput, processInput):
        if self.runnable:
            outputRaster = self.inputRasters[self.bandIndex]
            return createOutput('finished', outputRaster, constants.DTRASTER)
        
        return createOutput('error', "operation not runnable", constants.DTERROR)
           
def registerOperation():
     return ArrayElementOperation()