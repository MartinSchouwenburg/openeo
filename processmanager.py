import threading
from multiprocessing import Process, Queue
from datetime import datetime
from constants import constants
import common
import pickle
from pathlib import Path

def linkSection(begin, end):
        return {
                "href" :  begin + "/" + end,
                "rel" : 'self',
                "type" : "application/json"
            }
def makeBaseResponseDict(job_id, status, code, baseurl = None, message=None) :
    if status == constants.STATUSUNKNOWN:
        process = globalProcessManager.getProcess(None, job_id)
        if  process != None:
            status = process.status

    res = { "id" : job_id,
            "code" : code,
            "status" : status,
            "submitted" : str(datetime.now()),
        }
    if baseurl != None:
        res['links'] = linkSection(baseurl, job_id)
        
    if message != None:
        res['message'] = message
    return res

def ErrorResponse(id, code, message):
        return { "id" : id, "code" : code, "message" : message}

def worker(openeoprocess, outputQueue):
    openeoprocess.status = constants.STATUSRUNNING
    openeoprocess.run(outputQueue)

class OutputInfo:
    def __init__(self, eoprocess):
        self.eoprocess = eoprocess
        self.progress = 0
        self.last_updated = str(datetime.now())
        self.output = None
        self.status = constants.STATUSQUEUED
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
                    if self.processQueue[i].status == constants.STATUSCREATED:                    
                        self.processQueue[i].status = constants.STATUSQUEUED
                        return "Job " + str(job_id) + " is queued",""
                    else:
                        return "Job doesnt have correct status :"  + self.processQueue[i].status,constants.CUSTOMERROR
                else:
                    return "Job is owned by a different user", constants.CUSTOMERROR
            else: # its no longer in the processqueue so it might have shifted to the output list
                for jobb_id, item in self.outputs: 
                    if str(jobb_id) == job_id: #if its there the client shouldn't ask for queuing as it is already running/done/canceled
                        return "Job doesnt have correct status :"  + item.status, constants.CUSTOMERROR
                    
            return "Job isn't present in the system","JobNotFound"
                     
    def stopJob(self, job_id, user):
        with self.lockOutput:
            for key,value in self.outputs.items():
                if value.eoprocess.user == user:
                    if job_id == str(value.eoprocess.job_id):
                        value.eoprocess.stop()
                        return
                            

    def makeEstimate(self, user, job_id):
        eoprocess = self.getProcess(user, job_id)
        if eoprocess != None:
            return (eoprocess.estimate(user), 200)
        return ({'id' : job_id, 'code' : 'job not found'}, 400)

    def removedCreatedJob(self, job_id):
        for i in range(len(self.processQueue)):
            if str(self.processQueue[i].job_id) == job_id:
                if self.processQueue[i].status == constants.STATUSCREATED:
                    self.processQueue.pop(i)
                    return constants.STATUSCREATED
                else:
                    return constants.STATUSQUEUED
        return constants.STATUSUNKNOWN                
                


    def getProcess(self, user, job_id):
        for i in range(len(self.processQueue)):
            if str(self.processQueue[i].job_id) == job_id:
                return self.processQueue[i]
        for jobb_id, item in self.outputs: 
            if str(jobb_id) == job_id:
                return item.eoprocess
        return None            


    def allJobsMetadata4User(self, user, job_id, baseurl):
        with self.lockOutput:
            processes = []   
            for key,value in self.outputs.items():
                if value.eoprocess.user == user:
                    if job_id == None or ( job_id == str(value.eoprocess.job_id)):
                        dict = value.eoprocess.toDict( job_id == None)
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
            if job_id == None: ## case were a list of metadata is requested 
                return processes 
            if len(processes) == 1:                                       
                return processes[0]  # case were only on job is queried   
            return ''             

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
        self.loadProcessTables()
        startTimer = datetime.now()            
        while self.running:
            eoprocess = None
            with self.lockProcessQue:
                if not len(self.processQueue) == 0:
                    for p in self.processQueue:
                        if p.status == constants.STATUSQUEUED:
                            eoprocess = self.processQueue.pop()
                            break
            if eoprocess != None:
                p = Process(target=worker, args=(eoprocess,self.outputQueue))
                self.createNewEmptyOutput(eoprocess)
                self.outputs[str(eoprocess.job_id)].status = constants.STATUSRUNNING
                p.start()
            if self.outputQueue.qsize() > 0:
                self.changeOutputStatus()
            endTimer = datetime.now()
            if (endTimer - startTimer).seconds > 120:
                self.dumpProcessTables()
                startTimer = endTimer

    def loadProcessTables(self):
        path = common.openeoip_config['data_locations']['system_files']['location']
        path1 = Path(path + '/processqueue.bin')
        if path1.is_file():
            with open(path1, 'rb') as f:
                self.processQueue = pickle.load(f)
        path2 = Path(path + '/processoutputs.bin')
        if path2.is_file() :
             with open(path2, 'rb') as f:
                dump = pickle.load(f)
                for output in dump.items():
                    if output[1].status == constants.STATUSFINISHED:
                        self.outputs[output[1].eoprocess.job_id] = output[1]
                    elif output[1].status == constants.STATUSQUEUED:
                        self.processQueue.append(output[1].eoporocess)
                    elif output[1].status == constants.STATUSRUNNING:
                        self.processQueue.append(output[1].eoporocess)                        


    def changeOutputStatus(self):
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

    def dumpProcessTables(self):
        path = common.openeoip_config['data_locations']['system_files']['location']
        if len(self.processQueue) > 0:
            path1 = path + '/processqueue.bin'
            with open(path1, 'wb') as f:
                pickle.dump(self.processQueue, f)
        if len(self.outputs) > 0:                
            path2 = path + '/processoutputs.bin'
            with open(path2, 'wb') as f:
                pickle.dump(self.outputs, f)

globalProcessManager  = ProcessManager()

