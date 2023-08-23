#from workflow.worklfownode import WorkflowNode
import worklfownode
from executionnode import ExecutionNode
from estimationnode import EstimationNode
from openeooperation import *
from constants import constants
##from constants.constants import *


class Workflow(OpenEoOperation):

    def __init__(self, process_graph, getOperation):
        self.workflowGraph = {}
        self.outputNodes = []
        self.sourceGraph = process_graph
        self.getOperation = getOperation
        self.startNode = None
        for processKey,processValues in process_graph.items():
            grNode = worklfownode.WorkflowNode(processValues)
            self.workflowGraph[processKey] = grNode
            
        self.determineOutputNodes(self.workflowGraph)

    def validateNode(self, node):
        errors = []
        for arg in node.arguments.items():
                if ( node.argumentValues[arg[0]] == None): # ninput from other node
                    fromNodeId = arg[1]['from_node']
                    backNode = self.id2Node(fromNodeId)
                    errors = errors + self.validateNode(backNode[1])
                   
        processObj = self.getOperation(node.process_id)
        if processObj == None:
             errors.append("missing \'operation\' " + node.process_id  )

        return errors             

    def validateGraph(self):
            errors = []
            for node in self.outputNodes:
                errors = errors + self.validateNode(node[1])
            return errors                
                   
    def prepare(self, arguments):
        return ""
    
    def estimate(self):
        try:
            for node in self.outputNodes:
                self.startNode = EstimationNode(node,self)
                return self.startNode.estimate()

        except Exception as ex:
            return createOutput(False, str(ex), constants.DTERROR)

    def run(self,job_id, toServer, fromServer ):
        try:
            for node in self.outputNodes:
                self.startNode = ExecutionNode(node,self)
                self.startNode.run(job_id, toServer, fromServer)
                return self.startNode.outputInfo
        except Exception as ex:
            return createOutput(False, str(ex), constants.DTERROR)
        
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


  






