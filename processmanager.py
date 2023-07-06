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
        self.status = 'queued'
        self.logs = []

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
            self.outputs[str(eoprocess.job_id)] = OutputInfo(eoprocess)

    def addLog4job(self, job_id, logCount, level, message, data=None, usage=None, links=None):
            self.outputQueue.put({'type' : 'loggingevent', 'job_id': job_id, 'id' : logCount, 'level' : level, 'message' : message, 'time' : str(datetime.now())})

    def setOutput(self, id, output):
        with self.lockOutput:
            self.outputs[str(id)].output = output

    def addOutputProgress(self, id, progress):
        with self.lockOutput:
            self.outputs[str(id)].progress = progress

    def allJobs4User(self, user, processid):
        with self.lockOutput:
            processes = []   
            for key,value in self.outputs.items():
                if value.eoprocess.user.username == user.username:
                    if processid == None or ( processid == str(value.eoprocess.job_id)):
                        dict = value.eoprocess.toDict( processid == None)
                        dict['progress'] = value.progress
                        dict['updated'] = value.last_updated
                        dict['status'] = value.status
                        processes.append(dict)
            return processes                    

    def alllogs4job(self, user, jobid):
        with self.lockOutput:
            for key,value in self.outputs.items():
                if value.eoprocess.user.username == user.username:
                    if  jobid == str(value.eoprocess.job_id):
                        return value.logs
        return []                    
    
    
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
                    type = item['type']
                    if type == 'progressevent':
                        self.outputs[job_id].progress = item['progress']
                        self.outputs[job_id].last_updated = str(datetime.now())
                        self.outputs[job_id].status = item['status']
                    if type == 'logginevent':
                        del item['type']
                        self.outputs[job_id].logs.append(item)



globalProcessManager  = ProcessManager()

