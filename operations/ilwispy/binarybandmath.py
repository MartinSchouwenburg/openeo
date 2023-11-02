from operations.ilwispy.BaseMapCalc import BaseBinarymapCalcBase

class AddOperation(BaseBinarymapCalcBase):
    def __init__(self):
        self.loadOpenEoJsonDef('add.json')

    def prepare(self, arguments):
        self.base_prepare(arguments, '+')
        return ""

    def run(self, job_id, processOutput, processInput):
        return self.base_run(job_id, processOutput, processInput)

class DivideOperation(BaseBinarymapCalcBase):
    def __init__(self):
        self.loadOpenEoJsonDef('divide.json')

    def prepare(self, arguments):
        self.base_prepare(arguments, '/')
        return ""

    def run(self, job_id, processOutput, processInput):
        return self.base_run(job_id, processOutput, processInput)
    
class MultiplyOperation(BaseBinarymapCalcBase):
    def __init__(self):
        self.loadOpenEoJsonDef('multiply.json')

    def prepare(self, arguments):
        self.base_prepare(arguments, '*')
        return ""

    def run(self, job_id, processOutput, processInput):
        return self.base_run(job_id, processOutput, processInput) 
     
class SubtractOperation(BaseBinarymapCalcBase):
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