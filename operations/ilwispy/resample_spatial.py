from openeooperation import *
from operationconstants import *
from constants import constants

import openeo


class ResampleSpatial(OpenEoOperation):
    def __init__(self):
        self.loadOpenEoJsonDef('resample_spatial.json')
        
        self.kind = constants.PDPREDEFINED

    def prepare(self, arguments):
        self.runnable = False

        method = arguments['method']['resolved']
        if method == 'near':
            self.method = 'nearestneighbour'
        elif method == 'cubic':
            self.method = 'bicubic'
        elif method == 'bilinear':
            self.method = 'bilinear'
        else:
            return 'unsupported interpolation method: ' + method
        
        pixelSize  = arguments['resolution']['resolved']
        if pixelSize < 0:
            return 'resolution must be zero or greater'        

        data = arguments['data']['resolved']
        for r in data:
            if r.isValid():
                if type(r) is RasterData:
                    self.extra = self.constructExtraParams(r, r.temporalExtent, 0)                 
                    self.inputRaster = r.getRaster().rasterImp()                  
                    pixSize = r.getRaster().pixelSize()
                    if pixSize == 0:
                        self.pixelSize = pixSize
                    else:
                        self.pixelSize = pixelSize 
                else:
                    return 'no valid raster data in operation resample_spatial'                                           
           

        projection = arguments['projection']['resolved']
      

        if not isinstance(projection, int):
            return 'only epsg numbers allowed as projection definition'
        
        self.csy = ilwis.CoordinateSystem('epsg:' + str(projection))
        if bool(self.csy) == False:
            return 'Coordinate system invalid in resample_spatial'
        
        self.runnable = True

        return ""
              

    def run(self, job_id, processOutput, processInput):
        if self.runnable:
            put2Queue(processOutput, {'progress' : 0, 'job_id' : job_id, 'status' : 'running'})
            
            env = self.inputRaster.envelope()
            grf = ilwis.do('createcornersgeoreference', \
                           env.minCorner().x, env.minCorner().y, env.maxCorner().x, env.maxCorner().y, \
                           self.pixelSize, self.csy, True, '.')

            outputRc = ilwis.do("resample", self.inputRaster, grf, self.method)
            outputRasters = []                
            outputRasters.extend(self.setOutput([outputRc], self.extra))
            put2Queue(processOutput,{'progress' : 100, 'job_id' : job_id, 'status' : 'finished'}) 
            return createOutput('finished', outputRasters, constants.DTRASTER)  

        return createOutput('error', "operation no runnable", constants.DTERROR)
        
def registerOperation():
     return ResampleSpatial()