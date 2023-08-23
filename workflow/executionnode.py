from worklfownode import WorkflowNode
from constants import *
from openeooperation import * 
import copy
import sys
import traceback

class ExecutionNode :


    def __init__(self, node, workflow):
        self.workflowNode = node
        self.workflow = workflow
        self.outputInfo = None

   
    def run(self, job_id, queue, fromServer):
        ok = False        
        if self.workflowNode != None:
 
            if self.workflowNode[1].nodeType == WorkflowNode.CONDITION:
                ok = self.executeTest(job_id, queue, fromServer)
            elif self.workflowNode[1].nodeType == WorkflowNode.OPERATION:
                ok = self.executeOperation(job_id, queue, fromServer)
        return ok
        
    def executeTest(self, job_id, queue):
        return True
    
    def stop():
        return 0
    
    def executeOperation(self, job_id, toServer, fromServer):
        wfNode = self.workflowNode[1]
        for arg in wfNode.arguments.items():
            if ( wfNode.argumentValues[arg[0]] == None): # not calculated yet
                fromNodeId = arg[1]['from_node']
                backNode = self.workflow.id2Node(fromNodeId)
                exNode = ExecutionNode(backNode,self.workflow)
                if exNode.run():
                     self.workflowNode[1].argumentValues[arg[0]] = exNode.outputInfo["value"]
                else:
                    return False                     

        processNode = self.workflowNode[1]
        processObj = self.workflow.getOperation(processNode.process_id)
        if  processObj != None:
            arguments = processNode.argumentValues
            executeObj =  copy.deepcopy(processObj)
            message = executeObj.prepare(arguments)
            if not executeObj.runnable:
                self.outputInfo =  createOutput(False, message, DTERROR)
                return False

            try:
                self.outputInfo = executeObj.run(processOutput=toServer, processInput = fromServer, job_id=job_id)
                    
            except Exception:
                    e_type, e_value, e_tb = sys.exc_info()
                    traceback_model = dict(message=str(e_value),traceback=traceback.format_tb(e_tb),type=str(e_type))                       
                    self.outputInfo  = createOutput(False, str(traceback_model), DTERROR)
                    return False

        return True


