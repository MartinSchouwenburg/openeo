import threading
from multiprocessing import Process, Queue
from datetime import datetime
from constants.constants import *

def linkSection(begin, end):
        return {
                "href" :  begin + "/" + end,
                "rel" : 'self',
                "type" : "application/json"
            }
def makeBaseResponseDict(job_id, status, code, baseurl = None, message=None) :
    if status == STATUSUNKNOWN:
        process = globalProcessManager.getProcess(None, job_id)
        if  process != None:
            status = process.status

    res = { "job_id" : job_id,
            "code" : code,
            "status" : status,
            "submitted" : str(datetime.now()),
        }
    if baseurl != None:
        res['links'] = linkSection(baseurl, job_id)
        
    if message != None:
        res['message'] = message
    return res

def worker(openeoprocess, outputQueue):
    openeoprocess.run(outputQueue)

class OutputInfo:
    def __init__(self, eoprocess):
        self.eoprocess = eoprocess
        self.progress = 0
        self.last_updated = str(datetime.now())
        self.output = None
        self.status = STATUSQUEUED
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

    def queueJob(self, user, job_id):
         with self.lockProcessQue:
            idx = -1
            for i in range(len(self.processQueue)):
                if str(self.processQueue[i].job_id) == job_id:
                   idx = i
                   break
                   
            if idx != -1:
                if self.processQueue[i].user == user:
                    if self.processQueue[i].status == STATUSCREATED:                    
                        self.processQueue[i].status = STATUSQUEUED
                        return "Job is queued"
                    else:
                        return "Job doesnt have correct status :"  + self.processQueue[i].status
                else:
                    return "Job is owned by a different user"
            else: # its no longer in the processqueue so it might have shifted to the output list
                for jobb_id, item in self.outputs: 
                    if str(jobb_id) == job_id: #if its there the client shouldn't ask for queuing as it is already running/done/canceled
                        return "Job doesnt have correct status :"  + item.status
                    
            return "Job isn't present in the system"
                     
    def stopJob(self, user, job_id):
        with self.lockOutput:
            for key,value in self.outputs.items():
                if value.eoprocess.user == user:
                    if job_id == str(value.eoprocess.job_id):
                        value.eoprocess.stop()

    def makeEstimate(self, user, job_id):
        eoprocess = self.getProcess(user, job_id)
        if eoprocess != None:
            return (eoprocess.estimate(user), 200)
        return ({'id' : job_id, 'code' : 'job not found'}, 400)

    def removedCreatedJob(self, job_id):
        for i in range(len(self.processQueue)):
            if str(self.processQueue[i].job_id) == job_id:
                if self.processQueue[i].status == STATUSCREATED:
                    self.processQueue.pop(i)
                    return STATUSCREATED
                else:
                    return STATUSQUEUED
        return STATUSUNKNOWN                
                


    def getProcess(self, user, job_id):
        for i in range(len(self.processQueue)):
            if str(self.processQueue[i].job_id) == job_id:
                return self.processQueue[i]
        for jobb_id, item in self.outputs: 
            if str(jobb_id) == job_id:
                return item.eoprocess
        return None            


    def allJobs4User(self, user, processid, baseurl):
        with self.lockOutput:
            processes = []   
            for key,value in self.outputs.items():
                if value.eoprocess.user == user:
                    if processid == None or ( processid == str(value.eoprocess.job_id)):
                        dict = {} ##value.eoprocess.toDict( processid == None)
                        dict['progress'] = value.progress
                        dict['updated'] = value.last_updated
                        dict['status'] = value.status
                        dict['job_id'] = value.eoprocess.job_id
                        dict['submitted'] = value.eoprocess.submitted
                        dict["links"]  = {
                            "href" :  baseurl + "/" + value.eoprocess.job_id,
                            "rel" : 'self',
                            "type" : "application/json"
                            }
                        processes.append(dict)
            return processes                    

    def alllogs4job(self, user, jobid):
        with self.lockOutput:

            for key,value in self.outputs.items():
                if value.eoprocess.user == user:
                    if  jobid == str(value.eoprocess.job_id):
                        logs = []
                        for log in value.logs:
                            logEntry = {}
                            logEntry['timestamp'] = log.timestamp
                            logEntry['message'] = log.message
                            logEntry['level'] = log.level
                            logs.append(logEntry) 
                        return logs                           
        return []                    
    
    
    def stop(self):
        self.running = False

    def startProcesses(self):
        while self.running:
            eoprocess = None
            with self.lockProcessQue:
                if not len(self.processQueue) == 0:
                    for p in self.processQueue:
                        if p.status == STATUSQUEUED:
                            eoprocess = self.processQueue.pop()
                            break
            if eoprocess != None:
                p = Process(target=worker, args=(eoprocess,self.outputQueue))
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

