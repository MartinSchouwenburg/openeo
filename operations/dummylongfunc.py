from openeooperation import *
from operations.operationconstants import *
from constants.constants import *
from datetime import datetime


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
                response = {}
                b = 0
                lim = int(self.a * 100)
                i = 0
                t1 = datetime.timestamp(datetime.now())
                for i in range(0,lim):
                    b = self.a * i

                t2 = datetime.timestamp(datetime.now())

                b = t2 - t1                   

                return createOutput(True, b, DTNUMBER)
            
            return createOutput(False, "operation no runnable", DTERROR)

def registerOperation():
     return DummyLongFunc()