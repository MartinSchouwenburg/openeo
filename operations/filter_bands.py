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
                message =  "invalid input. Number of rasters is 0 in operation:" + self.name
                common.logMessage(logging.ERROR, message)
                return message         
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
                        message =  'Band list doesn match available bands'
                        common.logMessage(logging.ERROR, message)
                        return message                        
                if 'wavelenghts' in arguments:
                    requestedWavelengths = arguments['wavelengths']['resolved']
                    

        except:
            return "error" 

    def run(self, job_id, processOutput, processInput):
        if self.runnable:
            self.logStartOperation(processOutput, job_id)
            outData = []
            for raster in self.inpData:
                    for bandItem in raster.bands:
                        if self.bands != None:
                            if bandItem['name'] in self.bands:
                                outData.append(raster)
            self.logEndOperation(processOutput, job_id)
            return createOutput('finished', outData, constants.DTRASTER)
        common.notRunnableError(job_id) 
        return createOutput('error', "operation not runnable", constants.DTERROR)   

def registerOperation():
    return FilterBands()               