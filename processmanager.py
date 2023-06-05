import threading


class OutputInfo:
    def __init__(self):
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
            self.processQueue.append(eoproces)

    def createNewEmptyOutput(self, id):
        with self.lockOutput:
            self.outputs[id] = OutputInfo()

    def setOutput(self, id, output):
        with self.lockOutput:
            self.outputs[id].output = output

    def addOutputProgress(self, id, progress):
        with self.lockOutput:
            self.outputs[id].progress = progress
    
    def stop(self):
        self.running = False

    def startProcesses(self):
        while self.running:
            eoprocess = None
            with self.lockProcessQue:
                if not len(self.processQueue) == 0:
                    eoprocess = self.processQueue.pop()
            if eoprocess != None:
                eoprocess.run()

globalProcessManager  = ProcessManager()

