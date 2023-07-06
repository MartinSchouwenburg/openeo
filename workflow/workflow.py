from workflow.worklfownode import WorkflowNode
from workflow.executionnode import ExecutionNode
from openeooperation import *
from constants.constants import *


class Workflow(OpenEoOperation):

    def __init__(self, process_graph, getOperation):
        self.workflowGraph = {}
        self.outputNodes = []
        self.sourceGraph = process_graph
        self.getOperation = getOperation
        for processKey,processValues in process_graph.items():
            grNode = WorkflowNode(processValues)
            self.workflowGraph[processKey] = grNode
            
        self.determineOutputNodes(self.workflowGraph)

    def prepare(self, arguments):
        return ""
    
    def run(self,job_id, queue ):
        try:
            for node in self.outputNodes:
                exNode = ExecutionNode(node,self)
                exNode.run(job_id, queue)
                return exNode.outputInfo
        except:
            return createOutput(False, "Unknown exception", DTERROR)

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


  






