from openeooperation import *
from operationconstants import *
from constants import constants
from common import openeoip_config

class SaveResultOperation(OpenEoOperation):
    def __init__(self):
        self.loadOpenEoJsonDef('save_result.json')
        
        self.kind = constants.PDPREDEFINED

    def prepare(self, arguments):
        self.runnable = False
        self.format = arguments['format']['resolved']
        self.data = arguments['data']['resolved']
        self.options = arguments['options']['resolved']
        self.runnable = True
        return ""
              

    def run(self, job_id, processOutput, processInput):
        if self.runnable:
            self.logStartOperation(processOutput, job_id)
            path = openeoip_config['data_locations']['root_user_data_location']
            path = path['location'] + '/' + str(job_id)    
            os.makedirs(path)
            if self.data != None:
                for d in self.data:
                    name = d.getRaster().name()
                    name = name.replace('_ANONYMOUS', 'raster')
                    outpath = path + '/' + name
                    d.getRaster().rasterImp().store("file://" + outpath,self.format, "gdal")
                

                ext = ('.tif','.dat','.mpr','.tiff','.jpg', '.png')
                file_names = [f for f in os.listdir(path) if f.endswith(ext)]
                files = []
                for filename in file_names:
                    fn = path + "/"  + filename
                    files.append(fn)
            self.logEndOperation(processOutput, job_id)
            return createOutput('finished', files, constants.DTRASTERLIST)
        message = common.notRunnableError(job_id)
        return createOutput('error', message, constants.DTERROR)
        
def registerOperation():
     return SaveResultOperation()