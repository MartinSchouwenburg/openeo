import json
from pathlib import Path
import os
import pickle
from multiprocessing import Lock
import logging

lock = Lock()

current_dir = os.path.dirname(os.path.abspath(__file__))
configPath = os.path.join(current_dir,'config/config.json' )
openeoip_configfile = open(configPath)
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

def saveIdDatabase(idDatabse):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        home = Path.home()
        loc = openeoip_config['data_locations']['system_files']
        sytemFolder = os.path.join(home, loc['location'])
        propertiesFolder = os.path.join(home, sytemFolder)
        if ( not os.path.exists(propertiesFolder)):
            os.makedirs(propertiesFolder)
        propsPath = os.path.join(propertiesFolder, 'id2filename.table')
        propsFile = open(propsPath, 'wb')
        pickle.dump(idDatabse, propsFile)
        propsFile.close() 

def makeFolder(path):
    try:
        if ( not os.path.exists(path)):
            logger = logging.getLogger('openeo')
            logger.log(logging.INFO, 'could not open:'+ path)
            os.makedirs(path)
    except Exception as ex:
        raise Exception('server error. could not make:' + path)         
