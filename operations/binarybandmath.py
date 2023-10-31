from mapCalcBase import mapCalcBase2

class AddOperation(mapCalcBase2):
    def __init__(self):
        self.loadOpenEoJsonDef('add.json')

    def prepare(self, arguments):
        self.base_prepare(arguments, '+')
        return ""

    def run(self, job_id, processOutput, processInput):
        return self.base_run(job_id, processOutput, processInput)

class DivideOperation(mapCalcBase2):
    def __init__(self):
        self.loadOpenEoJsonDef('divide.json')

    def prepare(self, arguments):
        self.base_prepare(arguments, '/')
        return ""

    def run(self, job_id, processOutput, processInput):
        return self.base_run(job_id, processOutput, processInput)
    
class MultiplyOperation(mapCalcBase2):
    def __init__(self):
        self.loadOpenEoJsonDef('multiply.json')

    def prepare(self, arguments):
        self.base_prepare(arguments, '*')
        return ""

    def run(self, job_id, processOutput, processInput):
        return self.base_run(job_id, processOutput, processInput) 
     
class SubtractOperation(mapCalcBase2):
    def __init__(self):
        self.loadOpenEoJsonDef('subtract.json')

    def prepare(self, arguments):
        self.base_prepare(arguments, '-')
        return ""

    def run(self, job_id, processOutput, processInput):
        return self.base_run(job_id, processOutput, processInput)      
       
def registerOperation():
    funcs = []     
    funcs.append(AddOperation())
    funcs.append(DivideOperation())
    funcs.append(MultiplyOperation()) 
    funcs.append(SubtractOperation())           


    return funcs