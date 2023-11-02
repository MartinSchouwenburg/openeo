from openeooperation import *
from operationconstants import *
from constants import constants
import math
from rasterdata import RasterData

class BaseUnarymapCalc(OpenEoOperation):
    def base_prepare(self, arguments, oper):
        try:
            self.runnable = False
            self.rasterSizesEqual = True

            if len(arguments) != 1:
                return  createOutput(False,"number of parameters is not correct",  constants.DTERROR)
            it = iter(arguments)
            p1 = arguments[next(it)]['resolved']
            if isinstance(p1, list):
                rasterList = []
                for ras in p1:
                    if type(ras) is RasterData:
                        extra = self.constructExtraParams(ras, ras.temporalExtent, 0)
                        raster = ras.getRaster().rasterImp()
                        rasterList.append({'raster' : raster, 'extra' : extra})
                    self.parmValue = rasterList                        
                        
            else:
                if math.isnan(p1):
                    return createOutput(False, "the parameter a is not a number", constants.DTERROR)
                self.parmValue = p1                        
            self.operation = oper
            self.runnable = True                                      
                
        except Exception as ex:
            return ""

    def base_run(self, job_id, processOutput, processInput):
        if self.runnable:

            put2Queue(processOutput, {'progress' : 0, 'job_id' : job_id, 'status' : 'running'})
            if isinstance(self.parmValue, list):
                outputRasters = []                                
                for item in self.parmValue:
                    oper = self.operation + '(@1)'
                    outputRc = ilwis.do('mapcalc', oper, item['raster'])

                outputRasters.extend(self.setOutput([outputRc], item['extra']))
                out =  createOutput('finished', outputRasters, constants.DTRASTER)                
            else:
                c = eval(self.operation + '(' + self.parmValue + ')')
                out = createOutput('finished', c, constants.DTNUMBER)

            put2Queue(processOutput,{'progress' : 100, 'job_id' : job_id, 'status' : 'finished'}) 
            return out
            
        return createOutput('error', "operation no runnable", constants.DTERROR)
    
class BaseBinarymapCalcBase(OpenEoOperation):
    def base_prepare(self, arguments, oper):
        try:
            self.runnable = False
            self.rasterSizesEqual = True

            if len(arguments) != 2:
                return  createOutput(False,"number of parameters is not correct",  constants.DTERROR)
            it = iter(arguments)
            self.p1 = arguments[next(it)]['resolved']
            self.p2 = arguments[next(it)]['resolved']
            self.mapcalc = type(self.p1) is RasterData or type(self.p2) is RasterData

            if not type(self.p1) is RasterData:
                if math.isnan(self.p1):
                    return createOutput(False, "the parameter a is not a number", constants.DTERROR)
            if not type(self.p2) is RasterData:
                if math.isnan(self.p2):
                    return createOutput(False, "the parameter b is not a number", constants.DTERROR)                              
    
            self.runnable = True

            if type(self.p1) is RasterData:
                self.extra = self.constructExtraParams(self.p1, self.p1.temporalExtent, 0)
                self.p1 = self.p1.getRaster().rasterImp()
            if type(self.p2) is RasterData:
                self.extra = self.constructExtraParams(self.p2, self.p2.temporalExtent, 0)                 
                self.p2 = self.p2.getRaster().rasterImp()
            self.operation = oper                           
                
        except Exception as ex:
            return ""

    def base_run(self, job_id, processOutput, processInput):
        if self.runnable:

            put2Queue(processOutput, {'progress' : 0, 'job_id' : job_id, 'status' : 'running'})

            if self.mapcalc:
                oper = '@1' + self.operation + '@2'
                outputRc = ilwis.do("mapcalc", oper, self.p1,self.p2)
                outputRasters = []                
                outputRasters.extend(self.setOutput([outputRc], self.extra))
                out =  createOutput('finished', outputRasters, constants.DTRASTER)                
            else:
                c = self.a * self.b
                out = createOutput('finished', c, constants.DTNUMBER)

            put2Queue(processOutput,{'progress' : 100, 'job_id' : job_id, 'status' : 'finished'}) 
            return out
            
        return createOutput('error', "operation no runnable", constants.DTERROR)                        