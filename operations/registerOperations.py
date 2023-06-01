from openeooperation import OpenEoOperation
#from operations.multiply import MultiplyOperation
#from operations.dummylongfunc import DummyLongFunc
import os
import importlib

def initOperationMetadata():



# Specify the subdirectory path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Get a list of all Python files in the subdirectory
    file_names = [f for f in os.listdir(current_dir) if f.endswith('.py')]
    subdirectory = 'operations'
    # Iterate over the file names
    operationsMetaData = {}
    for file_name in file_names:
        # Remove the file extension to get the module name
        module_name = file_name[:-3]

        # Import the module dynamically
        module = importlib.import_module(f'{subdirectory}.{module_name}', package=__package__)
        

        if hasattr(module, 'registerOperation'):
            opObject = module.registerOperation()
            operationsMetaData[opObject.name] = opObject


        
       # o1 = MultiplyOperation()
       # operationsMetaData[o1.name] = o1

        #o1 = DummyLongFunc()
        # operationsMetaData[o1.name] = o1
 

    return operationsMetaData