from enum import Enum
import uuid
from typing import Set, Dict, Optional, Tuple, Union
from workflow.worklfownode import WorkflowNode
from workflow.executionnode import ExecutionNode
from openeooperation import *
from globals import globalsSingleton
from constants.constants import *

class Worklflow(OpenEoOperation):

    def __init__(self, process_graph):
        self.workflowGraph = {}
        self.outputNodes = []
        self.job_id = uuid.uuid4() 
        self.sourceGraph = process_graph
        for processKey,processValues in process_graph.items():
            grNode = WorkflowNode(processValues)
            self.workflowGraph[processKey] = grNode
            
        self.determineOutputNodes(self.workflowGraph)

    def prepare(self, arguments):
        return ""
    
    def run(self,waituntilfinished ):
        try:
            for node in self.outputNodes:
                exNode = ExecutionNode(node,self)
                exNode.run()
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


  





