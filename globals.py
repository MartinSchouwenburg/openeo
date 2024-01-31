import os
import json
from pathlib import Path
import pickle
from operations.registerOperations import initOperationMetadata 
from constants import constants
import datetime

def getOperation(operationName)        :
    if  operationName in globalsSingleton.operations:
        return globalsSingleton.operations[operationName]
    return None

class Globals : 
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Globals, cls).__new__(cls)
        return cls.instance

    openeoip_config = None
    internal_database = {}
    operations = initOperationMetadata(getOperation)

    def initGlobals(self):
        if  self.openeoip_config == None:
            openeoip_configfile = open('./config/config.json')
            self.openeoip_config = json.load(openeoip_configfile)
            codesfile = open('./config/default_error_codes.json')
            self.default_errrors = json.load(codesfile)                    
      

    def insertRasterInDatabase(self, raster):
        self.internal_database[raster.id] = raster

    def filepath2raster(self, filename):
        items = self.internal_database.items()
        for item in items:
            if item[0] == filename:
                return item[1]
        return '?' 
    
    def id2Raster(self, id):
        items = self.internal_database.items()
        #if size ==0 then the scan on data location has not happened so we look into the saved properties of a previous scan
        if len(items) == 0:
            if self.loadIdDatabase():
                items = self.internal_database.items()
       
        for item in items:
            p = item[0]
            if p == id:
                raster = item[1]
                mttime = datetime.datetime.fromtimestamp(os.path.getmtime(raster.dataSource))
                if mttime == raster.lastmodified:
                    return raster
        return None        
    
    def saveIdDatabase(self):
        home = Path.home()
        loc = globalsSingleton.openeoip_config['data_locations']['system_files']
        sytemFolder = os.path.join(home, loc['location'])
        propertiesFolder = os.path.join(home, sytemFolder)
        if ( not os.path.exists(propertiesFolder)):
            os.makedirs(propertiesFolder)
        propsPath = os.path.join(propertiesFolder, 'id2filename.table')
        propsFile = open(propsPath, 'wb')
        pickle.dump(self.internal_database, propsFile)
        propsFile.close() 

    def loadIdDatabase(self):
        home = Path.home()
        loc = globalsSingleton.openeoip_config['data_locations']['system_files']
        sytemFolder = os.path.join(home, loc['location'])        
        propertiesFolder = os.path.join(home, sytemFolder)
        if ( not os.path.exists(propertiesFolder)):
            return False
        
        propertiesPath = os.path.join(propertiesFolder, 'id2filename.table')
        if ( os.path.exists(propertiesPath)):
            file_stats = os.stat(propertiesPath)
            if file_stats.st_size > 0:
                with open(propertiesPath, 'rb') as f:
                    data = f.read()
                self.internal_database = pickle.loads(data) 
                return True
        return False            
        
    def errorJson(self, errorStringCode, id, message):
        if errorStringCode == constants.CUSTOMERROR:
            return {"id" : id, "code" : 400, "message" : message }
        else:
            if errorStringCode in self.default_errrors:
                predefCode = self.default_errrors[errorStringCode].http                    
                return {"id" : id, "code" : predefCode, "message" : message }
                
        return {"id" : id, "code" : 400, "message" : message }

    
        
globalsSingleton = Globals()

                






