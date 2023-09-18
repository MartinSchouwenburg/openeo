from openeooperation import *
from operationconstants import *
from constants import constants
import json

class LoadCollectionOperation(OpenEoOperation):
    def __init__(self):
        self.loadOpenEoJsonDef('load_collection.json')
      
        self.kind = constants.PDPREDEFINED


    def prepare(self, arguments):
        self.runnable = False

        return ""
              

    def run(self, job_id, processOutput, processInput):
        if self.runnable:

        
            return createOutput('finished', 42, constants.DTNUMBER)
        
        return createOutput('error', "operation no runnable", constants.DTERROR)
        
def registerOperation():
     return LoadCollectionOperation()