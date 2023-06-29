import threading
from multiprocessing import Process

def worker(openeoprocess):
    openeoprocess.run()

class OutputInfo:
    def __init__(self, eoprocess):
        self.eoprocess = eoprocess
        self.progress = 0
        self.output = None

    def isFinished(self):
        return self.progress == 1

class ProcessManager:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ProcessManager, cls).__new__(cls)
        return cls.instance
      
    def __init__(self):
        self.lockProcessQue = threading.Lock()
        self.lockOutput = threading.Lock()
        self.processQueue  = []
        self.outputs = {}
        self.running = True

    def addProcess(self, eoproces):
        with self.lockProcessQue:
            self.processQueue.append( eoproces)

    def createNewEmptyOutput(self, eoprocess):
        with self.lockOutput:
            self.outputs[eoprocess.workflow.job_id] = OutputInfo(eoprocess)
            ii = id(self)  
            print(ii)

    def setOutput(self, id, output):
        with self.lockOutput:
            self.outputs[id].output = output

    def addOutputProgress(self, id, progress):
        with self.lockOutput:
            self.outputs[id].progress = progress

    def allJobs4User(self, user):
        with self.lockOutput:
            processes = []   
            ii = id(self)
            print(ii)         
            for key,value in self.outputs.items():
                if value.eoprocess.user.username == user.username:
                    dict = value.eoprocess.toDict()
                    processes.append(dict)
            return processes                    


    
    def stop(self):
        self.running = False

    def startProcesses(self):
        while self.running:
            eoprocess = None
            with self.lockProcessQue:
                if not len(self.processQueue) == 0:
                    eoprocess = self.processQueue.pop()
            if eoprocess != None:
                p = Process(target=worker, args=(eoprocess,))
                self.createNewEmptyOutput(eoprocess)
                p.start()
                print(id(self))

globalProcessManager  = ProcessManager()

