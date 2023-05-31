import os
import json
from pathlib import Path
import pickle
import glob
from openeooperation import OpenEoOperation
from operations.registerOperations import initOperationMetadata 

class Globals : 
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Globals, cls).__new__(cls)
        return cls.instance

    openeoip_config = None
    internal_database = {}
    operations = initOperationMetadata()

    def initGlobals(self):
        if  self.openeoip_config == None:
            openeoip_configfile = open('./config/config.json')
            self.openeoip_config = json.load(openeoip_configfile)
      

    def insertFileNameInDatabase(self, dataid, filepath):
        if filepath in self.internal_database:
            return
        self.internal_database[filepath] = dataid

    def filepath2id(self, filename):
        items = self.internal_database.items()
        for item in items:
            if item[0] == filename:
                return item[1]
        return '?' 
    
    def id2filepath(self, id):
        items = self.internal_database.items()
        #if size ==0 then the scan on data location has not happened so we look into the saved properties of a previous scan
        if len(items) == 0:
            self.loadIdDatabase()
            items = self.internal_database.items()
       
        for item in items:
            if str(item[1]) == id:
                return item[0]
        return ''        
    
    def saveIdDatabase(self):
        home = Path.home()
        propertiesFolder = os.path.join(home, 'Documents/openeo/properties')
        if ( not os.path.exists(propertiesFolder)):
            os.makedirs(propertiesFolder)
        propsPath = os.path.join(propertiesFolder, 'id2filename.table')
        propsFile = open(propsPath, 'wb')
        pickle.dump(self.internal_database, propsFile)
        propsFile.close() 

    def loadIdDatabase(self):
        home = Path.home()
        propertiesFolder = os.path.join(home, 'Documents/openeo/properties')
        if ( not os.path.exists(propertiesFolder)):
            return False
        
        propertiesPath = os.path.join(propertiesFolder, 'id2filename.table')
        if ( os.path.exists(propertiesPath)):
            with open(propertiesPath, 'rb') as f:
                data = f.read()
            self.internal_database = pickle.loads(data) 
            return True
        
    
        
globalsSingleton = Globals()

                






