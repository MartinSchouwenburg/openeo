from pathlib import Path
from workflow import processGraph
import os
import importlib
import json

def initOperationMetadata(getOperation):

# Specify the subdirectory path
    operationsMetaData = {}
    current_dir = os.path.dirname(os.path.abspath(__file__))
    subfolders = [ f.path for f in os.scandir(current_dir) if f.is_dir() ]
    for folder in subfolders:
        operationsMetaData = loadOperationsFolder(folder, operationsMetaData)                   

    operationsMetaData = loadOperationsFolder(current_dir,operationsMetaData)
  
    home = Path.home()
    openeoip_configfile = open('./config/config.json')
    openeoip_config = json.load(openeoip_configfile)
    udf_locations = openeoip_config["data_locations"]["udf_locations"]
    for udf_location in udf_locations:
        location = udf_location["location"]
        udfFolder = os.path.join(home, location)
        file_names = [f for f in os.listdir(udfFolder) if f.endswith('.udf')]
        for filename in file_names:
            udfpath = os.path.join(udfFolder, filename)        
            f = open(udfpath)
            data = json.load(f)
            processValues = data['process']
            wf = processGraph.ProcessGraph(processValues['process_graph'], None, getOperation)
            operationsMetaData[processValues['id']] = wf

    return operationsMetaData

def loadOperationsFolder(folder,operationsMetaData):
    file_names = [f for f in os.listdir(folder) if f.endswith('.py')]
    if len(file_names) == 0:
        return operationsMetaData
    
    parts = folder.split(os.sep)
    foldername = parts[-1]
    subdirectory = foldername
    for filename in file_names:
        module_name = filename[:-3]

            # Import the module dynamically
        try:
            module = importlib.import_module(f'{subdirectory}.{module_name}', package=__package__)
           
            if hasattr(module, 'registerOperation'): 
                opObject = module.registerOperation()
                if isinstance(opObject, list):
                    for func in opObject:
                        operationsMetaData[func.name] = func 
                else:                   
                    operationsMetaData[opObject.name] = opObject
        except Exception as ex:
            continue

    return operationsMetaData