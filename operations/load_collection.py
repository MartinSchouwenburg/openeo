from openeooperation import *
from operationconstants import *
from constants import constants
from rasterdata import *
from common import getRasterDataSets
import ilwis
from pathlib import Path

class LoadCollectionOperation(OpenEoOperation):
    def __init__(self):
        self.loadOpenEoJsonDef('load_collection.json')
      
        self.kind = constants.PDPREDEFINED
        self.bandIdxs = []
        self.lyrIdxs = []

    def prepare(self, arguments):
        try:
            self.runnable = False            
            self.inputRaster = getRasterDataSets()[arguments['id']]
            if self.inputRaster == None:
                return "NotFound"
            
            self.dataSource = ''
            folder = ''
            if  self.inputRaster.type == 'file':
                self.dataSource = self.inputRaster.dataSource
                folder = os.path.dirname(os.path.abspath(self.dataSource))
            else:
                folder = self.dataSource = self.inputRaster.dataFolder

            
            if 'bands'in arguments :
                if arguments['bands'] != None:
                    self.bandIdxs = self.inputRaster.getBandIndexes(arguments['bands'])
                else:
                    self.bandIdxs.append(0)
            else:
                self.bandIdxs.append(0)

            if 'temporal_extent' in arguments:
                self.temporalExtent = arguments['temporal_extent']
                if arguments['temporal_extent'] != None:
                    self.lyrIdxs = self.inputRaster.getLayerIndexes(arguments['temporal_extent'])
                else:
                    self.lyrIdxs.append(0)                

            path = Path(folder).as_uri()
            ilwis.setWorkingCatalog(path)
            self.runnable = True
            self.rasterSizesEqual = True
 
        except Exception as ex:
            return ""

        return ""
   
    def run(self, job_id, processOutput, processInput):
        if self.runnable:
            outputRasters = []
            indexes = str(self.bandIdxs).lstrip('[').rstrip(']')
            ext = self.inputRaster.spatialExtent
            env = str(ext[0]) + " " + str(ext[2]) + "," + str(ext[1]) + " " +str(ext[3])
            for idx in indexes:
                bandIdxList = 'rasterbands(' + idx + ')'
                rasters = []
                for lyrIdx in self.lyrIdxs:
                    layer = self.inputRaster.idx2layer(lyrIdx)
                    if layer != None:    
                        datapath = os.path.join(self.dataSource, layer.dataSource)
                        rband = ilwis.RasterCoverage(datapath)
                        rc = ilwis.do("selection", rband, "envelope(" + env + ") with: " + bandIdxList)
                        rasters.append(rc)

                extra = self.constructExtraParams(self.inputRaster, self.temporalExtent, idx)
                outputRasters.extend(self.setOutput(rasters, extra))


            return createOutput('finished', outputRasters, constants.DTRASTER)
        
        return createOutput('error', "operation not runnable", constants.DTERROR)
           
def registerOperation():
     return LoadCollectionOperation()