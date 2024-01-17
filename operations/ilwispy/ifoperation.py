from openeooperation import *
from operationconstants import *
from constants import constants

def __init__(self):
        self.loadOpenEoJsonDef('if.json')
        
        self.kind = constants.PDPREDEFINED

def prepare(self, arguments):
        ##TODO
        self.runnable = False
                         
        return ''  

def run(self, job_id, processOutput, processInput):
    if self.runnable:
         return None
    
    return createOutput('error', "operation no runnable", constants.DTERROR)      