from operations.ilwispy.BaseMapCalc import BaseUnarymapCalc

class ArcCosOperation(BaseUnarymapCalc):
    def __init__(self):
        self.loadOpenEoJsonDef('arccos.json')

    def prepare(self, arguments):
        self.base_prepare(arguments, 'acos')
        return ""

    def run(self, job_id, processOutput, processInput):
        return self.base_run(job_id, processOutput, processInput)
    
class CosOperation(BaseUnarymapCalc):
    def __init__(self):
        self.loadOpenEoJsonDef('cos.json')

    def prepare(self, arguments):
        self.base_prepare(arguments, 'cos')
        return ""

    def run(self, job_id, processOutput, processInput):
        return self.base_run(job_id, processOutput, processInput)    

class ASinOperation(BaseUnarymapCalc):
    def __init__(self):
        self.loadOpenEoJsonDef('arcsin.json')

    def prepare(self, arguments):
        self.base_prepare(arguments, 'asin')
        return ""

    def run(self, job_id, processOutput, processInput):
        return self.base_run(job_id, processOutput, processInput)
        
class SinOperation(BaseUnarymapCalc):
    def __init__(self):
        self.loadOpenEoJsonDef('sin.json')

    def prepare(self, arguments):
        self.base_prepare(arguments, 'sin')
        return ""

    def run(self, job_id, processOutput, processInput):
        return self.base_run(job_id, processOutput, processInput)

class TanOperation(BaseUnarymapCalc):
    def __init__(self):
        self.loadOpenEoJsonDef('tan.json')

    def prepare(self, arguments):
        self.base_prepare(arguments, 'tan')
        return ""

    def run(self, job_id, processOutput, processInput):
        return self.base_run(job_id, processOutput, processInput)

class ATanOperation(BaseUnarymapCalc):
    def __init__(self):
        self.loadOpenEoJsonDef('arctan.json')

    def prepare(self, arguments):
        self.base_prepare(arguments, 'atan')
        return ""

    def run(self, job_id, processOutput, processInput):
        return self.base_run(job_id, processOutput, processInput)             

def registerOperation():
     funcs = []
     funcs.append(ArcCosOperation())
     funcs.append(CosOperation())     
     funcs.append(SinOperation()) 
     funcs.append(ASinOperation()) 
     funcs.append(TanOperation()) 
     funcs.append(ATanOperation())                         

     return funcs