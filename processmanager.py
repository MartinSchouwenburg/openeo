import threading
from multiprocessing import Process, Queue
from datetime import datetime

def worker(openeoprocess, outputQueue):
    openeoprocess.run(outputQueue)

class OutputInfo:
    def __init__(self, eoprocess):
        self.eoprocess = eoprocess
        self.progress = 0
        self.last_updated = str(datetime.now())
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
        self.outputQueue = Queue()
        self.running = True


    def addProcess(self, eoproces):
        with self.lockProcessQue:
            self.processQueue.append( eoproces)

    def createNewEmptyOutput(self, eoprocess):
        with self.lockOutput:
            self.outputs[eoprocess.job_id] = OutputInfo(eoprocess)


    def setOutput(self, id, output):
        with self.lockOutput:
            self.outputs[id].output = output

    def addOutputProgress(self, id, progress):
        with self.lockOutput:
            self.outputs[id].progress = progress

    def allJobs4User(self, user, name):
        with self.lockOutput:
            processes = []   
            for key,value in self.outputs.items():
                if value.eoprocess.user.username == user.username:
                    if name == None or ( name == str(value.eoprocess.job_id)):
                        dict = value.eoprocess.toDict( name == None)
                        dict['progress'] = value.progress
                        dict['updated'] = value.last_updated
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
                p = Process(target=worker, args=(eoprocess,self.outputQueue,))
                self.createNewEmptyOutput(eoprocess)
                p.start()
            if self.outputQueue.qsize() > 0:
                item = self.outputQueue.get()
                job_id = item['job_id']
                if job_id in self.outputs:
                    self.outputs[job_id].progress = item['progress']
                    self.outputs[job_id].last_update = str(datetime.now())


globalProcessManager  = ProcessManager()

