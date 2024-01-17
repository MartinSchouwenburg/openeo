from openeooperation import *
from operationconstants import *
from constants import constants
from rasterdata import RasterData

class FilterBands(OpenEoOperation):
    def __init__(self):
        self.loadOpenEoJsonDef('filter_bands.json') 

    def prepare(self, arguments):
        try:
            self.runnable = False 
            self.inpData = arguments['data']['resolved']
            if len(self.inpData) == 0:
                return 'invalid input. Number of rasters is 0'            
            if isinstance(self.inpData[0], RasterData):
                if 'bands' in arguments:
                    requestedBands = arguments['bands']['resolved']
                    foundCount = 0
                    for item in self.inpData:
                        for bandItem in item.bands:
                            if bandItem['name'] in requestedBands:
                                foundCount = foundCount + 1
                    if foundCount == len(requestedBands):
                        self.bands = requestedBands                    
                        self.runnable = True
                    else:
                        return 'Band list doesn match available bands'
                if 'wavelenghts' in arguments:
                    requestedWavelengths = arguments['wavelengths']['resolved']
                    

        except:
            return "error" 

    def run(self, job_id, processOutput, processInput):
        if self.runnable:
            outData = []
            for raster in self.inpData:
                    for bandItem in raster.bands:
                        if self.bands != None:
                            if bandItem['name'] in self.bands:
                                outData.append(raster)

            return createOutput('finished', outData, constants.DTRASTER)
        
        return createOutput('error', "operation not runnable", constants.DTERROR)   

def registerOperation():
    return FilterBands()               