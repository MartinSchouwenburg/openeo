from workflow.worklfownode import WorkflowNode
from workflow.executionnode import ExecutionNode
from workflow.estimationnode import EstimationNode
from openeooperation import *
from constants.constants import *


class Workflow(OpenEoOperation):

    def __init__(self, process_graph, getOperation):
        self.workflowGraph = {}
        self.outputNodes = []
        self.sourceGraph = process_graph
        self.getOperation = getOperation
        self.startNode = None
        for processKey,processValues in process_graph.items():
            grNode = WorkflowNode(processValues)
            self.workflowGraph[processKey] = grNode
            
        self.determineOutputNodes(self.workflowGraph)

    def prepare(self, arguments):
        return ""
    
    def estimate(self):
        try:
            for node in self.outputNodes:
                self.startNode = EstimationNode(node,self)
                return self.startNode.estimate()

        except Exception as ex:
            return createOutput(False, str(ex), DTERROR)

    def run(self,job_id, toServer, fromServer ):
        try:
            for node in self.outputNodes:
                self.startNode = ExecutionNode(node,self)
                self.startNode.run(job_id, toServer, fromServer)
                return self.startNode.outputInfo
        except Exception as ex:
            return createOutput(False, str(ex), DTERROR)
        
    def stop(self):
        if self.startNode != None:
            self.startNode.stop()

    def processGraph(self):
        return self.sourceGraph
    

    def id2Node(self, id):
        for node in self.workflowGraph.items():
            if node[0] == id:
                return node
        return None            

    def determineOutputNodes(self, nodes):
        for node in nodes.items():
            if hasattr(node[1], 'result'):
                self.outputNodes.append(node)


  






