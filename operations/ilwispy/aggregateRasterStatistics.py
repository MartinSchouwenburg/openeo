from constants import constants
from operations.ilwispy.BaseAggregatestats import BaseAggregateData

class MaxOperation(BaseAggregateData):
    def __init__(self):
        self.loadOpenEoJsonDef('max.json')
      
        self.kind = constants.PDPREDEFINED

    def prepare(self, arguments):
        try:
            it = iter(arguments)
            p1 = arguments[next(it)]['resolved']
            self.method = 'max'
            if isinstance(p1, list):
                self.base_prepareRaster(arguments)
                self.method = 'max'
            self.runnable = True

        except Exception as ex:
            return ""

        return ""

    def run(self, job_id, processOutput, processInput):
        return self.base_run(job_id, processOutput, processInput)
    
class MeanOperation(BaseAggregateData):
    def __init__(self):
        self.loadOpenEoJsonDef('mean.json')
      
        self.kind = constants.PDPREDEFINED

    def prepare(self, arguments):
        try:
            self.base_prepareRaster(arguments)
            self.method = 'mean'
            self.runnable = True

        except Exception as ex:
            return ""

        return ""

    def run(self, job_id, processOutput, processInput):
        return self.base_run(job_id, processOutput, processInput) 

class MedianOperation(BaseAggregateData):
    def __init__(self):
        self.loadOpenEoJsonDef('median.json')
      
        self.kind = constants.PDPREDEFINED

    def prepare(self, arguments):
        try:
            self.base_prepareRaster(arguments)
            self.method = 'median'
            self.runnable = True

        except Exception as ex:
            return ""

        return ""

    def run(self, job_id, processOutput, processInput):
        return self.base_run(job_id, processOutput, processInput) 

class MinOperation(BaseAggregateData):
    def __init__(self):
        self.loadOpenEoJsonDef('min.json')
      
        self.kind = constants.PDPREDEFINED

    def prepare(self, arguments):
        try:
            self.base_prepareRaster(arguments)
            self.method = 'min'
            self.runnable = True

        except Exception as ex:
            return ""

        return ""

    def run(self, job_id, processOutput, processInput):
        return self.base_run(job_id, processOutput, processInput) 

class SumOperation(BaseAggregateData):
    def __init__(self):
        self.loadOpenEoJsonDef('sum.json')
      
        self.kind = constants.PDPREDEFINED

    def prepare(self, arguments):
        try:
            self.base_prepareRaster(arguments)
            self.method = 'sum'
            self.runnable = True

        except Exception as ex:
            return ""

        return ""

    def run(self, job_id, processOutput, processInput):
        return self.base_run(job_id, processOutput, processInput)             
class VarianceOperation(BaseAggregateData):
    def __init__(self):
        self.loadOpenEoJsonDef('variance.json')
      
        self.kind = constants.PDPREDEFINED

    def prepare(self, arguments):
        try:
            self.base_prepareRaster(arguments)
            self.method = 'variance'
            self.runnable = True

        except Exception as ex:
            return ""

        return ""

    def run(self, job_id, processOutput, processInput):
        return self.base_run(job_id, processOutput, processInput)
    
class StandardDevOperation(BaseAggregateData):
    def __init__(self):
        self.loadOpenEoJsonDef('sd.json')
      
        self.kind = constants.PDPREDEFINED

    def prepare(self, arguments):
        try:
            self.base_prepareRaster(arguments)
            self.method = 'standarddev'
            self.runnable = True

        except Exception as ex:
            return ""

        return ""

    def run(self, job_id, processOutput, processInput):
        return self.base_run(job_id, processOutput, processInput)    
    
def registerOperation():
    funcs = []     
    funcs.append(MaxOperation())
    funcs.append(MeanOperation())
    funcs.append(MedianOperation()) 
    funcs.append(MinOperation())           
    funcs.append(SumOperation()) 
    funcs.append(VarianceOperation())           
    funcs.append(StandardDevOperation())           


    return funcs