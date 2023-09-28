import json
from pathlib import Path
import os
import pickle
from multiprocessing import Lock

lock = Lock()

openeoip_configfile = open('./config/config.json')
openeoip_config = json.load(openeoip_configfile)

codesfile = open('./config/default_error_codes.json')
default_errrors = json.load(codesfile) 

raster_data_sets = None

def getRasterDataSets():
    home = Path.home()
    loc = openeoip_config['data_locations']['system_files']
    sytemFolder = os.path.join(home, loc['location'])        
    propertiesFolder = os.path.join(home, sytemFolder)
    if ( os.path.exists(propertiesFolder)):
        propertiesPath = os.path.join(propertiesFolder, 'id2filename.table')
        if ( os.path.exists(propertiesPath)):
            lock.acquire()
            with open(propertiesPath, 'rb') as f:
                data = f.read()
            f.close()
            lock.release()    
            raster_data_sets =  pickle.loads(data) 
    return raster_data_sets            
