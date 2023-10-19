from openeooperation import *
from operationconstants import *
from constants import constants
import math

class MultiplyOperation(OpenEoOperation):
    def __init__(self):
        self.loadOpenEoJsonDef('multiply.json')
        self.kind = constants.PDPREDEFINED

        self.a = constants.UNDEFNUMBER
        self.b = constants.UNDEFNUMBER

    def prepare(self, arguments):
        self.runnable = False
        self.rasterSizesEqual = True

        if len(arguments) != 2:
            return  createOutput(False,"number of parameters is not correct",  constants.DTERROR)
        it = iter(arguments)
        self.a = arguments[next(it)]['resolved']
        self.b = arguments[next(it)]['resolved']
        self.mapcalc = type(self.a) is RasterData or type(self.b) is RasterData

        if not type(self.a) is RasterData:
            if math.isnan(self.a):
                return createOutput(False, "the parameter a is not a number", constants.DTERROR)
        if not type(self.b) is RasterData:
            if math.isnan(self.b):
                return createOutput(False, "the parameter b is not a number", constants.DTERROR)                              
 
        self.runnable = True
        return ""
              

    def run(self, job_id, processOutput, processInput):
        if self.runnable:

            put2Queue(processOutput, {'progress' : 0, 'job_id' : job_id, 'status' : 'running'})

            if self.mapcalc:
                p1 = self.a
                p2 = self.b
                outputRasters = []
                if type(self.a) is RasterData:
                    p1 = p1.ilwisRaster
                    extra = self.constructExtraParams(self.a, self.a.temporalExtent, 0)
                if type(self.b) is RasterData:
                    p2 = p2.ilwisRaster
                    extra = self.constructExtraParams(self.b, self.b.temporalExtent, 0)

                outputRc = ilwis.do("mapcalc", '@1 * @1', p1,p2)
                outputRasters.extend(self.setOutput([outputRc], extra))
                out =  createOutput('finished', outputRasters, constants.DTRASTER)                
            else:
                c = self.a * self.b
                out = createOutput('finished', c, constants.DTNUMBER)

            put2Queue(processOutput,{'progress' : 100, 'job_id' : job_id, 'status' : 'finished'}) 
            return out
            
        
        return createOutput('error', "operation no runnable", constants.DTERROR)
        
def registerOperation():
     return MultiplyOperation()
  




