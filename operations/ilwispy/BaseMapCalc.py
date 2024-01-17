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
            if self.operation in ['pow']:
                self.operation = 'power'
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
                c = eval('math.' + self.operation + '(' + self.parmValue + ')')
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
            self.ismaps1 = isinstance(self.p1, list)## maps are always in lists; numbers not
            self.ismaps2 = isinstance(self.p2, list)

            if not self.ismaps1: 
                if math.isnan(self.p1):
                    return createOutput(False, "the parameter a is not a number", constants.DTERROR)
            if not self.ismaps2:
                if math.isnan(self.p2):
                    return createOutput(False, "the parameter b is not a number", constants.DTERROR)                              
    
            self.runnable = True

            if self.ismaps1:
                self.rasters1 = self.extractRasters(self.p1)
            if self.ismaps2 :
                self.rasters2 = self.extractRasters(self.p2)

            self.operation = oper                           
                
        except Exception as ex:
            return ""

    def extractRasters(self, rasters):
        rasterImpls = []
        for idx in range(len(rasters)):
            r = rasters[idx]
            self.createExtra(r, idx) 
            rasterImpl = r.getRaster().rasterImp()
            rasterImpls.append(rasterImpl)
        return rasterImpls            

   

    def base_run(self, job_id, processOutput, processInput):
        if self.runnable:

            put2Queue(processOutput, {'progress' : 0, 'job_id' : job_id, 'status' : 'running'})

            outputRasters = [] 
            oper = '@1' + self.operation + '@2' 
            outputs = []                               
            if self.ismaps1 and self.ismaps2:
                for idx in len(self.rasters1):
                    outputRc = ilwis.do("mapcalc", oper, self.rasters1[idx],self.rasters2[idx])
                    outputs.append(outputRc)
            elif self.ismaps1 and not self.ismaps2:
                    for idx in range(len(self.rasters1)):
                        outputRc = ilwis.do("mapcalc", oper, self.rasters1[idx],self.p2)
                        outputs.append(outputRc)
            elif not self.ismaps1 and self.ismaps2:
                    for idx in range(len(self.rasters2)):
                        outputRc = ilwis.do("mapcalc", oper, self.p1,self.rasters2[idx])
                        outputs.append(outputRc)  
            else:
                output = None
                if self.operation in ['+','-', '/', '*', '<=', '>=', '==', 'or','and', 'xor']:
                    expr = str(self.p1) + self.operation + str(self.p2)
                    output = eval(expr)
                elif self.operation in ['log']:
                    expr = 'math.' + self.operation + '(' + str(self.p1)+ ',' +  str(self.p2) + ')'
                    output = eval(expr)
                out = createOutput('finished', output, constants.DTNUMBER) 

            if self.ismaps1 or self.ismaps2:
                outputRasters.extend(self.setOutput(outputs, self.extra))
                out =  createOutput('finished', outputRasters, constants.DTRASTER)                
              
                

            put2Queue(processOutput,{'progress' : 100, 'job_id' : job_id, 'status' : 'finished'}) 
            return out
            
        return createOutput('error', "operation no runnable", constants.DTERROR)                        