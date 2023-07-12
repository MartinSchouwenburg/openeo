from workflow.worklfownode import WorkflowNode
from constants.constants import *
from openeooperation import * 
import copy
import datetime

class EstimationNode:
    def __init__(self, node, workflow):
        self.workflowNode = node
        self.workflow = workflow
        self.estimationInfo = { 'cost' : 0, 'duration' : 0, 'size' : 0, 'expires' : datetime.datetime(2100,1,1)}

    def estimate(self):
        if self.workflowNode != None:
            if self.workflowNode[1].nodeType == WorkflowNode.CONDITION:
                self.merge(self.estimateTest())
            elif self.workflowNode[1].nodeType == WorkflowNode.OPERATION:
                return self.estimateOperation()
        return self.estimationInfo
    
    def merge(self, estimatiomInfo):
        self.estimationInfo['cost'] = self.estimationInfo['cost'] + estimatiomInfo['cost']
        self.estimationInfo['duration'] = self.estimationInfo['duration'] + estimatiomInfo['duration']
        self.estimationInfo['size'] = self.estimationInfo['size'] + estimatiomInfo['size']
        self.estimationInfo['expires'] = min([self.estimationInfo['expires'], estimatiomInfo['expires']])


    
    def noEstimate(self):
        outputInfo = { 'outputdimensions' : [], 'outputtype' : DTUNKNOWN, 'outputsubtype' : DTUNKNOWN}
        outputcost = { 'cost' : 0, 'duration' : 0, 'size' :0, 'expires' : datetime.datetime(2100,1,1)}

        return (False, outputInfo, outputcost)
    
    def estimateTest(self):
        return self.noEstimate()
    
    def estimateOperation(self):
        wfNode = self.workflowNode[1]
        for arg in wfNode.estimationValues.items():
            if ( wfNode.estimationValues[arg[0]] == None): # not calculated yet
                fromNodeId = arg[1]['from_node']
                backNode = self.workflow.id2Node(fromNodeId)
                exNode = EstimationNode(backNode,self.workflow)
                estimate = exNode.estimate()
                if estimate[0] == False:
                    return self.noEstimate();
            
                self.workflowNode[1].estimationValues[arg[0]] = estimate[1]                
                self.merge(estimate[2])

        processNode = self.workflowNode[1]
        processObj = self.workflow.getOperation(processNode.process_id)
        arguments = processNode.estimationValues
        executeObj =  copy.deepcopy(processObj)
        if hasattr(executeObj, 'estimate'):
            estimate = executeObj.estimate(processNode.estimationValues, processNode.argumentValues)
            if estimate[0] == False:
                return self.noEstimate();
            self.merge(estimate[2])
            return (True, estimate[1], self.estimationInfo)

        
        return self.noEstimate()       
     
