from openeooperation import *
from operationconstants import *
from constants import constants
from rasterdata import RasterData
from enum import Enum


class MergeCubes(OpenEoOperation):
    def __init__(self):
         self.loadOpenEoJsonDef('merge_cubes.json') 

    def prepare(self, arguments):
        try:
            self.runnable = False
            targetRasters = arguments['cube1']['resolved'] 
            mergeRasters = arguments['cube2']['resolved']
            self.mergeCases = []
            lenTarget = len(targetRasters)
            lenMerge = len(mergeRasters)
            if lenTarget != lenMerge:
                return 'Raster can be merged due to incompatible numbers'
            for idx in range(lenTarget):
                targetRaster = self.targetRasters[idx]
                mergeRaster = self.mergeRasters[idx]                            
                self.mergeCases.append({'target' : targetRaster, 'merge': mergeRaster, 'mergeCondition' :self.determineMergeCondition(targetRaster, mergeRaster)})
            self.runnable = True     

        except:
            return "error" 

    def run(self, job_id, processOutput, processInput):
        if self.runnable:
            return None
        lenTarget = len(self.targetRasters)
        for idx in range(lenTarget):
            ilwRaster = self.targerRaster[idx].getRaster().rasterImp()
            rcClone = ilwRaster.clone()
            mergeRaster = self.targerRaster[idx]
            mergeIlwRaster = mergeRaster.getRaster().rasterImp()
            rc = ilwis.do("mergeraster", rcClone, mergeIlwRaster)



                
                
        return createOutput('error', "operation not runnable", constants.DTERROR)  
    
    def nameUnique(self, targetBands, name):
        for targetBand in targetBands:
            if name == targetBand['name']:
                return False
        return True
                
    def determineMergeCondition(self, targetRaster : RasterData, mergeRaster : RasterData):
        result = {'nameclash' : [], 'sizesEqual' : False, 'projectionsUnequal' : False}

        
        for mergeBand in mergeRaster.bands:
            result['nameclash'].append({'name': mergeBand['name'], 'unique' : self.nameUnique(targetRaster.bands,mergeBand['name']) })

        result['projectionsUnequal'] = targetRaster.epsg != mergeRaster.epsg
        
        spExtentTarget = targetRaster.spatialExtent
        spExtentMerge = mergeRaster.spatialExtent
        result['sizesEqual']  = self.checkSpatialDimensions([spExtentTarget, spExtentMerge]) 
       
        return result

def registerOperation():
    return MergeCubes()               