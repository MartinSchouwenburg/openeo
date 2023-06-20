from openeooperation import *
from operations.operationconstants import *
from constants.constants import *
import time


class DummyLongFunc(OpenEoOperation):
    def __init__(self):

        self.name = 'dummylongfunc'
        self.description = 'dummy function that does nothing but run for some time. needed for testing'
        self.summary = 'dummy needed fror testing'
        self.categories = ['test']
        self.exceptions['DummyError'] = { 'message': 'I am dumb'}

        self.addInputParameter('a', 'why not', OPERATION_SCHEMA_NUMBER)

        self.addOutputParameter('to complete things',OPERATION_SCHEMA_NUMBER)
        self.kind = PDUSERDEFINED

        self.a = UNDEFNUMBER

    def prepare(self, arguments):
            self.runnable = True

            self.a = arguments['a']

            return ""

    def run(self, waituntilfinished):
            if self.runnable:
                time.sleep(40.0)

                return createOutput(True, 23, DTNUMBER)
            
            return createOutput(False, "operation no runnable", DTERROR)

def registerOperation():
     return DummyLongFunc()