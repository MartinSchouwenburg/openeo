from estimationnode import EstimationNode
from openeooperation import *
from constants import constants
import copy
##from constants.constants import *

class ProcessNode :
    constants.UNDEFINED = 0
    OPERATION = 1
    JUNCTION = 2
    CONDITION = 3

    def __init__(self, parentProcessGraph, nodeDict, nodeName):
        self.nodeName = nodeName ## just for easy identification; doesnt play a role on this level
        self.parentProcessGraph = parentProcessGraph
        for key, pValue in nodeDict.items():
            if key == 'process_id':
                self.process_id = pValue
            elif key == 'arguments':
                self.localArguments = {}
                for key, value in pValue.items():
                    self.localArguments[key] = { 'base' : value, 'resolved' : None}

            elif key == 'description':
                self.description = pValue
            elif key == 'result':
                self.result = pValue
               
            self.nodeType = ProcessNode.OPERATION 
            self.nodeValue = None

class ProcessGraph(OpenEoOperation):

    def __init__(self, source_graph, arguments, getOperation):
        self.processGraph = {}
        self.outputNodes = []
        self.sourceGraph = source_graph
        self.processArguments = arguments
        self.localArguments = {}
        self.getOperation = getOperation
        self.startNode = None
        for processKey,processValues in source_graph.items():
            grNode = ProcessNode(self, processValues, processKey)
            self.processGraph[processKey] = grNode
            
        self.determineOutputNodes(self.processGraph)

    def determineOutputNodes(self, nodes):
        for node in nodes.items():
            if hasattr(node[1], 'result'):
                self.outputNodes.append(node)

    def validateNode(self, node):
        errors = []
        for arg in node.localArguments.items():
                if ( arg[1]['resolved'] == None): # input needed from other node
                    base = arg[1]['base']
                    if isinstance(base, dict):
                        if 'from_node' in base:
                            fromNodeId = base['from_node']
                            backNode = self.id2node(fromNodeId)
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
            for key, processNode in self.outputNodes:
                self.startNode = NodeExecution(processNode,self)
                self.startNode.run(job_id, toServer, fromServer)
                return self.startNode.outputInfo
        except Exception as ex:
            return createOutput(False, str(ex), constants.DTERROR)
        
    def stop(self):
        if self.startNode != None:
            self.startNode.stop()

    def processGraph(self):
        return self.sourceGraph
    

    def id2node(self, id):
        for node in self.processGraph.items():
            if node[0] == id:
                return node
        return None            

    def determineOutputNodes(self, nodes):
        for node in nodes.items():
            if hasattr(node[1], 'result'):
                self.outputNodes.append(node) 

    def resolveParameter(self, parmKey):
        if parmKey in self.processArguments:
            return self.processArguments[parmKey]
        #assume its the process builder key/name which is unknown to us as its a client something
        return {'resolved': self.processArguments[0]}

class NodeExecution :

    def __init__(self, processNode, processGraph):
        self.processNode = processNode
        self.processGraph = processGraph
        self.outputInfo = None
        self.indirectKeys = ['from_parameter', 'from_node', 'reducer']

    def run(self, job_id, toServer, fromServer):
        args = self.processNode.localArguments
        for key, parmDef in args.items():
            if parmDef['resolved'] == None:
                definition = parmDef['base']
                if isinstance(definition, dict):
                   for item in definition.items():
                        if item[0] in self.indirectKeys:
                            resolvedValue = self.resolveNode(job_id, toServer, fromServer, item)
                        else:            
                            resolvedValue = self.resolveNode(job_id, toServer, fromServer, (key, definition)) 
                else:
                    resolvedValue = self.resolveNode(job_id, toServer, fromServer, (key, definition))                        
                args[key]['resolved'] = resolvedValue

        processObj = self.processGraph.getOperation(self.processNode.process_id)
        if  processObj != None:
            ##arguments = self.processNode.argumentValues
            executeObj =  copy.deepcopy(processObj)
            args['serverChannel'] = toServer
            args['job_id'] = job_id
            message = executeObj.prepare(args)
            if  executeObj.runnable:
                try:                
                    self.outputInfo = executeObj.run(job_id, toServer, fromServer) 
                except Exception:
                    return 'error'                    
            else:                               
                self.outputInfo =  createOutput(False, message, constants.DTERROR)
                return False
        return ''
    
    def mapcalc(self, args, pgraph):
        if self.checkBandMath(pgraph):

            flow = []
            for processKey,processValues in pgraph.items():
                node = {'id' : None, 'operation': None, 'referred_parm' : [], 'values' : []}
                for pkey, pValue in processValues.items():
                    if pkey == 'process_id':
                        node['id'] = processKey
                        node['operation'] = pValue
                    elif pkey == 'arguments':
                        for key, value in pValue.items():
                            if key == 'data':
                                if 'from_parameter' in value:
                                    node['referred_parm'].append(value['from_parameter'])
                            elif isinstance(value, dict) and 'from_node' in value:
                                node['values'].append('@@'+ value['from_node'])
                            else:
                                node['values'].append(value)
                flow.append(node)


    def checkBandMath(self, pgraph):
        bandmathOperation = True
        bandmathOperations = [ 'multiply', 'subtract', 'divide', 'add']
        for processKey,processValues in pgraph.items():
            for key, pValue in processValues.items():
                if key == 'process_id':
                    if not pValue in bandmathOperations:
                        if pValue != 'array_element':
                            bandmathOperation = False 

        return bandmathOperation                                                                                                                

   
    def resolveNode(self, job_id, toServer, fromServer, parmKeyValue):
        if 'from_node' in parmKeyValue:
            referredNodeName = parmKeyValue[1]
            referredNode = self.processGraph.id2node(referredNodeName)
            if referredNode != None:
                if referredNode[1].nodeValue == None:
                    refExecutionNode = NodeExecution(referredNode[1], self.processGraph)
                    if refExecutionNode.run(job_id, toServer, fromServer) == '':
                        referredNode[1].nodeValue = refExecutionNode.outputInfo
                        return referredNode[1].nodeValue['value']
                    return 'hmm'
        elif 'from_parameter' in parmKeyValue:
                refNode = self.processNode.parentProcessGraph.resolveParameter(parmKeyValue[1])
                if refNode['resolved'] != None:
                    return refNode['resolved'] 
                return self.resolveNode(job_id, toServer, fromServer, refNode)  
        elif 'reducer' in parmKeyValue:
            pgraph = parmKeyValue[1]['process_graph']
            args = self.processNode.localArguments
            self.mapcalc(args,pgraph)
            process = ProcessGraph(pgraph, args, self.processGraph.getOperation)
            self.outputInfo = process.run(job_id, toServer, fromServer)
            return self.outputInfo['value']
        else:
            return parmKeyValue[1]                                              