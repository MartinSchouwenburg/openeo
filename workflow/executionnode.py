from workflow.worklfownode import WorkflowNode
from constants.constants import *
from openeooperation import * 
import copy
import sys
import traceback

class ExecutionNode :


    def __init__(self, node, workflow, getOperation):
        self.workflowNode = node
        self.workflow = workflow
        self.outputInfo = None
        self.getOperation = getOperation

    def run(self):
        ok = False        
        if self.workflowNode != None:
 
            if self.workflowNode[1].nodeType == WorkflowNode.CONDITION:
                ok = self.executeTest()
            elif self.workflowNode[1].nodeType == WorkflowNode.OPERATION:
                ok = self.executeOperation()
        return ok
        
    def executeTest():
        return True
    
    def executeOperation(self):
        wfNode = self.workflowNode[1]
        noOfArguments = len(wfNode.arguments)
        for arg in wfNode.arguments.items():
            if ( wfNode.argumentValues[arg[0]] == None): # not calculated yet
                fromNodeId = arg[1]['from_node']
                backNode = self.workflow.id2Node(fromNodeId)
                exNode = ExecutionNode(backNode,self.workflow, self.getOperation)
                if exNode.run():
                     self.workflowNode[1].argumentValues[arg[0]] = exNode.outputInfo["value"]
                else:
                    return False                     

        processNode = self.workflowNode[1]
        processObj = self.getOperation(processNode.process_id)
        if  processObj != None:
            arguments = processNode.argumentValues
            executeObj =  copy.deepcopy(processObj)
            message = executeObj.prepare(arguments)
            if not executeObj.runnable:
                self.outputInfo =  createOutput(False, message, DTERROR)
                return False

            try:
                self.outputInfo = executeObj.run(waituntilfinished=True)
                    
            except Exception:
                    e_type, e_value, e_tb = sys.exc_info()
                    traceback_model = dict(message=str(e_value),traceback=traceback.format_tb(e_tb),type=str(e_type))                       
                    self.outputInfo  = createOutput(False, str(traceback_model), DTERROR)
                    return False

        return True


