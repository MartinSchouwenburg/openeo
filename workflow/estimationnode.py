from constants import *
from openeooperation import * 
import copy
import datetime

class EstimationNode:
    def __init__(self, node, processGraph):
        self.processNode = node
        self.processGraph = processGraph
        self.estimationInfo = { 'costs' : 0, 'duration' : 0, 'size' : 0, 'expires' : datetime.datetime(2100,1,1), "downloads_included" : ""}

    def estimate(self):
        if self.processNode != None:
            return self.estimateOperation()
        return self.estimationInfo
    
    def merge(self, estimatiomInfo):
        self.estimationInfo['costs'] = self.estimationInfo['cost'] + estimatiomInfo['cost']
        self.estimationInfo['duration'] = self.estimationInfo['duration'] + estimatiomInfo['duration']
        self.estimationInfo['size'] = self.estimationInfo['size'] + estimatiomInfo['size']
        self.estimationInfo['expires'] = min([self.estimationInfo['expires'], estimatiomInfo['expires']])


    
    def noEstimate(self):
        outputInfo = { 'outputdimensions' : [], 'outputtype' : constants.DTUNKNOWN, 'outputsubtype' : constants.DTUNKNOWN}
        outputcost = { 'costs' : 0, 'duration' : 0, 'size' :0, 'expires' : datetime.datetime(2100,1,1), "downloads_included" : ""}

        return (False, outputInfo, outputcost)
    
    def estimateTest(self):
        return self.noEstimate()
    
    def estimateOperation(self):
        wfNode = self.processNode[1]
        for arg in wfNode.estimationValues.items():
            if ( wfNode.estimationValues[arg[0]] == None): # not calculated yet
                fromNodeId = arg[1]['from_node']
                backNode = self.processGraph.id2Node(fromNodeId)
                exNode = EstimationNode(backNode,self.processGraph)
                estimate = exNode.estimate()
                if estimate[0] == False:
                    return self.noEstimate();
            
                self.processNode[1].estimationValues[arg[0]] = estimate[1]                
                self.merge(estimate[2])

        processNode = self.processNode[1]
        processObj = self.processGraph.getOperation(processNode.process_id)
        executeObj =  copy.deepcopy(processObj)
        if hasattr(executeObj, 'estimate'):
            estimate = executeObj.estimate(processNode.estimationValues, processNode.argumentValues)
            if estimate[0] == False:
                return self.noEstimate();
            self.merge(estimate[2])
            return (True, estimate[1], self.estimationInfo)

        
        return self.noEstimate()       
     
