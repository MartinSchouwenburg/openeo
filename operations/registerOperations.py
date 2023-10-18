from pathlib import Path
from workflow import processGraph
import os
import importlib
import json

def initOperationMetadata(getOperation):

# Specify the subdirectory path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Get a list of all Python files in the subdirectory
    file_names = [f for f in os.listdir(current_dir) if f.endswith('.py')]
    subdirectory = 'operations'
    # Iterate over the file names
    operationsMetaData = {}
    deltaWatch = {}
    for filename in file_names:
        # Remove the file extension to get the module name
        fullPath = os.path.join(current_dir,  filename)
        modifiedDate = int(os.path.getmtime(fullPath))
        if filename in deltaWatch:
            if modifiedDate == deltaWatch[filename]:
                continue

        module_name = filename[:-3]

        # Import the module dynamically
        module = importlib.import_module(f'{subdirectory}.{module_name}', package=__package__)
        

        if hasattr(module, 'registerOperation'):
            opObject = module.registerOperation()
            operationsMetaData[opObject.name] = opObject
            deltaWatch[filename] = modifiedDate

    # udf files
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
            modifiedDate = int(os.path.getmtime(udfpath))
            data = json.load(f)
            processValues = data['process']
            wf = processGraph.ProcessGraph(processValues['process_graph'], None, getOperation)
            operationsMetaData[processValues['id']] = wf
            deltaWatch[filename] = modifiedDate
        


    return operationsMetaData