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

class LogNOperation(BaseBinarymapCalcBase):
    def __init__(self):
        self.loadOpenEoJsonDef('log.json')

    def prepare(self, arguments):
        self.base_prepare(arguments, 'logn')
        return ""

    def run(self, job_id, processOutput, processInput):
        return self.base_run(job_id, processOutput, processInput) 

class GTOperation(BaseBinarymapCalcBase):
    def __init__(self):
        self.loadOpenEoJsonDef('gt.json')

    def prepare(self, arguments):
        self.base_prepare(arguments, '>')
        return ""

    def run(self, job_id, processOutput, processInput):
        return self.base_run(job_id, processOutput, processInput) 

class GTEOperation(BaseBinarymapCalcBase):
    def __init__(self):
        self.loadOpenEoJsonDef('gte.json')

    def prepare(self, arguments):
        self.base_prepare(arguments, '>=')
        return ""

    def run(self, job_id, processOutput, processInput):
        return self.base_run(job_id, processOutput, processInput) 

class LTOperation(BaseBinarymapCalcBase):
    def __init__(self):
        self.loadOpenEoJsonDef('lt.json')

    def prepare(self, arguments):
        self.base_prepare(arguments, '<')
        return ""

    def run(self, job_id, processOutput, processInput):
        return self.base_run(job_id, processOutput, processInput) 

class LTEOperation(BaseBinarymapCalcBase):
    def __init__(self):
        self.loadOpenEoJsonDef('lte.json')

    def prepare(self, arguments):
        self.base_prepare(arguments, '<=')
        return ""

    def run(self, job_id, processOutput, processInput):
        return self.base_run(job_id, processOutput, processInput) 

class EqOperation(BaseBinarymapCalcBase):
    def __init__(self):
        self.loadOpenEoJsonDef('eq.json')

    def prepare(self, arguments):
        self.base_prepare(arguments, '==')
        return ""

    def run(self, job_id, processOutput, processInput):
        return self.base_run(job_id, processOutput, processInput) 

class OrOperation(BaseBinarymapCalcBase):
    def __init__(self):
        self.loadOpenEoJsonDef('or.json')

    def prepare(self, arguments):
        self.base_prepare(arguments, 'or')
        return ""

    def run(self, job_id, processOutput, processInput):
        return self.base_run(job_id, processOutput, processInput) 

class AndOperation(BaseBinarymapCalcBase):
    def __init__(self):
        self.loadOpenEoJsonDef('and.json')

    def prepare(self, arguments):
        self.base_prepare(arguments, 'and')
        return ""

    def run(self, job_id, processOutput, processInput):
        return self.base_run(job_id, processOutput, processInput) 

class XorOperation(BaseBinarymapCalcBase):
    def __init__(self):
        self.loadOpenEoJsonDef('xor.json')

    def prepare(self, arguments):
        self.base_prepare(arguments, 'xor')
        return ""

    def run(self, job_id, processOutput, processInput):
        return self.base_run(job_id, processOutput, processInput)                                      
    
def registerOperation():
    funcs = []     
    funcs.append(AddOperation())
    funcs.append(DivideOperation())
    funcs.append(MultiplyOperation()) 
    funcs.append(SubtractOperation()) 
    funcs.append(LogNOperation()) 
    funcs.append(GTOperation()) 
    funcs.append(GTEOperation()) 
    funcs.append(LTOperation()) 
    funcs.append(LTEOperation()) 
    funcs.append(EqOperation()) 
    funcs.append(OrOperation())
    funcs.append(AndOperation()) 
    funcs.append(XorOperation())                                        


    return funcs