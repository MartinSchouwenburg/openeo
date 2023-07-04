from openeooperation import *
from operations.operationconstants import *
from constants.constants import *
import math

class MultiplyOperation(OpenEoOperation):
    def __init__(self):

        self.name = 'multiply'
        self.description = 'Multiplies the two numbers `a` and `b` (*a * b*) and returns the computed product.\n\nNo-data values are taken into account so that `null` is returned if any element is such a value.\n\nThe computations follow [IEEE Standard 754](https://ieeexplore.ieee.org/document/8766229) whenever the processing environment supports it.'
        self.summary = 'Multiplication of two numbers'
        self.categories = ['math']
        self.exceptions['MultiplicandMissing'] = { 'message': 'Multiplication requires at least two number'}

        self.addInputParameter('a', 'The multiplier', OPERATION_SCHEMA_NUMBER)
        self.addInputParameter('b', 'The multiplicand', OPERATION_SCHEMA_NUMBER)

        self.addOutputParameter('The computed product of the two numbers',OPERATION_SCHEMA_NUMBER)

        self.examples.append({ 'arguments' : {'a' : 5, 'b' : 2.5}, 'returns' : 12.5})
        self.examples.append({ 'arguments' : {'a' : -2, 'b' : -4}, 'returns' : 8})
        self.examples.append({ 'arguments' : {'a' : 1, 'b' : None}, 'returns' : None})

        self.addLink('about', 'http://mathworld.wolfram.com/Product.html', 'Product explained by Wolfram MathWorld' )
        self.addLink('about', 'https://ieeexplore.ieee.org/document/8766229', 'IEEE Standard 754-2019 for Floating-Point Arithmetic')

        self.kind = PDPREDEFINED

        self.a = UNDEFNUMBER
        self.b = UNDEFNUMBER

    def prepare(self, arguments):
        self.runnable = False

        if len(arguments) != 2:
            return  createOutput(False,"number of parameters is not correct",  DTERROR)
        
        if math.isnan(arguments['a']):
            return createOutput(False, "the parameter a is not a number", DTERROR)
        self.a = arguments['a']
        
        if math.isnan(arguments['b']):
            return createOutput(False, "the parameter b is not a number", DTERROR)
        self.b = arguments['b']

        self.runnable = True
        return ""
              

    def run(self, job_id, processOutput):
        if self.runnable:
            response = {}
            c = self.a * self.b
            returnInfo = {"status" : True, "value" : c, "datatype" : DTNUMBER}
            return createOutput(True, c, DTNUMBER)
        
        return createOutput(False, "operation no runnable", DTERROR)
        
def registerOperation():
     return MultiplyOperation()
  




