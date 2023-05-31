class WorkflowNode:
    UNDEFINED = 0
    OPERATION = 1
    JUNCTION = 2
    CONDITION = 3

    def __init__(self, processValues):

        for key, pValue in processValues.items():
            if key == 'process_id':
                self.process_id = pValue
            if key == 'arguments':
                self.setArguments(pValue)
            if key == 'description':
                self.description = pValue
            if key == 'result':
                self.result = pValue
                
            # for the moment they are all operations until the 'if' node is implemented                    
            self.nodeType = WorkflowNode.OPERATION  

    def setArguments(self, inputs):
        self.arguments = inputs
        self.argumentValues = {}
        for item in inputs.items():
            key = item[0]
            if isinstance(item[1], dict):
                if ( 'from_node' in item[1]):
                    self.argumentValues[key] = None
                else:
                    self.argumentValues[key] = item[1]                    
            else:
                 self.argumentValues[key] = item[1]

        
