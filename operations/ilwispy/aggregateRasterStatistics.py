from constants import constants
from operations.ilwispy.BaseAggregatestats import BaseAggregateStats

class MaxOperation(BaseAggregateStats):
    def __init__(self):
        self.loadOpenEoJsonDef('max.json')
      
        self.kind = constants.PDPREDEFINED

    def prepare(self, arguments):
        try:
            self.base_prepare(arguments)
            self.method = 'max'
            self.runnable = True

        except Exception as ex:
            return ""

        return ""

    def run(self, job_id, processOutput, processInput):
        return self.base_run(job_id, processOutput, processInput)
    
class MeanOperation(BaseAggregateStats):
    def __init__(self):
        self.loadOpenEoJsonDef('mean.json')
      
        self.kind = constants.PDPREDEFINED

    def prepare(self, arguments):
        try:
            self.base_prepare(arguments)
            self.method = 'mean'
            self.runnable = True

        except Exception as ex:
            return ""

        return ""

    def run(self, job_id, processOutput, processInput):
        return self.base_run(job_id, processOutput, processInput) 

class MedianOperation(BaseAggregateStats):
    def __init__(self):
        self.loadOpenEoJsonDef('median.json')
      
        self.kind = constants.PDPREDEFINED

    def prepare(self, arguments):
        try:
            self.base_prepare(arguments)
            self.method = 'median'
            self.runnable = True

        except Exception as ex:
            return ""

        return ""

    def run(self, job_id, processOutput, processInput):
        return self.base_run(job_id, processOutput, processInput) 

class MinOperation(BaseAggregateStats):
    def __init__(self):
        self.loadOpenEoJsonDef('min.json')
      
        self.kind = constants.PDPREDEFINED

    def prepare(self, arguments):
        try:
            self.base_prepare(arguments)
            self.method = 'min'
            self.runnable = True

        except Exception as ex:
            return ""

        return ""

    def run(self, job_id, processOutput, processInput):
        return self.base_run(job_id, processOutput, processInput) 

class SumOperation(BaseAggregateStats):
    def __init__(self):
        self.loadOpenEoJsonDef('sum.json')
      
        self.kind = constants.PDPREDEFINED

    def prepare(self, arguments):
        try:
            self.base_prepare(arguments)
            self.method = 'sum'
            self.runnable = True

        except Exception as ex:
            return ""

        return ""

    def run(self, job_id, processOutput, processInput):
        return self.base_run(job_id, processOutput, processInput)             
class VarianceOperation(BaseAggregateStats):
    def __init__(self):
        self.loadOpenEoJsonDef('variance.json')
      
        self.kind = constants.PDPREDEFINED

    def prepare(self, arguments):
        try:
            self.base_prepare(arguments)
            self.method = 'variance'
            self.runnable = True

        except Exception as ex:
            return ""

        return ""

    def run(self, job_id, processOutput, processInput):
        return self.base_run(job_id, processOutput, processInput)
    
class StandardDevOperation(BaseAggregateStats):
    def __init__(self):
        self.loadOpenEoJsonDef('sd.json')
      
        self.kind = constants.PDPREDEFINED

    def prepare(self, arguments):
        try:
            self.base_prepare(arguments)
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