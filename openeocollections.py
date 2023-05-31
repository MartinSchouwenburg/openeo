import os
import pystac
import json
import uuid 
from flask import Flask, jsonify
from flask_restful import Api, Resource
##from globals import openeoip_config
from globals import globalsSingleton
from eoreader.reader import Reader
from eoreader.bands import *
from pathlib import Path
import pickle
import glob

class OpenEOIPCollections(Resource):
    def get(self):
        return jsonify(loadCollections()) 
    

def loadCollections():
    data_location = globalsSingleton.openeoip_config['data_locations']
       
    allJson = {}
    allCollections = []
    home = Path.home()
    cacheFolder = os.path.join(home, 'Documents/openeo/cache')
    if ( not os.path.exists(cacheFolder)):
        os.makedirs(cacheFolder)

    for location in data_location:
        path = location["location"]

        extraPath = os.path.join(path, 'metadata.json')
        extraMetadataAll = None
        if os.path.exists(extraPath):
            extraMd = open(extraPath)
            extraMetadataAll = json.load(extraMd)  
        files = os.listdir(path)
        for filename in files:
            if filename != 'metadata.json':
                fullPath = os.path.join(path,  filename)

                collectionJsonDict = checkCache(cacheFolder, 'base_'+ filename, fullPath)
                if ( collectionJsonDict == {}):
                    prod = Reader().open(fullPath)
                    extraMetadata = None
                    if filename in extraMetadataAll:
                        extraMetadata = extraMetadataAll[filename]
                        
                    collectionJsonDict = createCollectionJson(prod, extraMetadata, fullPath)
                    save2Cache(collectionJsonDict, fullPath, 'base_' + filename, cacheFolder)
                else:
                    globalsSingleton.insertFileNameInDatabase(collectionJsonDict["id"], fullPath)

                allCollections.append(collectionJsonDict)

    allJson["collections"] = allCollections
    allJson["links"] = globalsSingleton.openeoip_config['links']

    globalsSingleton.saveIdDatabase() 

    return allJson    


def save2Cache(collectionDict, fullPath, filename, cacheFolder):
    modifiedData = int(os.path.getmtime(fullPath))
    cacheName = filename + '_' + str(modifiedData) + '.cache'
    cachePath = os.path.join(cacheFolder, cacheName)
    cacheFile = open(cachePath, 'wb')
    pickle.dump(collectionDict, cacheFile)
    cacheFile.close()

def checkCache(cacheFolder, filename, fullPath):
        modifiedData = int(os.path.getmtime(fullPath))
        cacheName = filename + '_' + str(modifiedData) + '.cache'
        cachePath = os.path.join(cacheFolder, cacheName)
        if ( os.path.exists(cachePath)):
            with open(cachePath, 'rb') as f:
                data = f.read()
            collectionJsonDict = pickle.loads(data) 
            return collectionJsonDict
        else:
            cacheName = filename + '_*' + '.cache'
            cachePath = os.path.join(cacheFolder, cacheName)
            oldfiles = glob.glob(cachePath)
            for oldfilename in oldfiles:
                os.remove(oldfilename)
        return {}
         
def createCollectionJson(product, extraMetadata, fullpath, id=None):
    stac_version = globalsSingleton.openeoip_config['stac_version']
    toplvl_dict = {'stac_version' : stac_version, 
                   'type' : 'Collection', 
                   'id' : product.stac.id, 
                   'title' : product.stac.title,
                   'description' : getExtra('description', extraMetadata, 'None'), 
                   'extent' : createExtentPart(product),
                   'license' : getExtra('license', extraMetadata, 'unknown'),                   
                   'keywords' : getExtra('keywords', extraMetadata, ''),
                   'providers' : getExtra('providers', extraMetadata, 'unknown'),
                   'links' : getExtra('links', extraMetadata, [])
                   }
  
    globalsSingleton.insertFileNameInDatabase(product.stac.id, fullpath)
    
    return toplvl_dict

def createExtentPart(product) :
    bbox = {}
    bbox['bbox'] = [product.stac.bbox]
    time = [str(product.stac.datetime), str(product.stac.datetime)]
    interval = {}
    interval['interval'] = [time]
    ext = {'spatial' : bbox, 'temporal' : interval}

    return ext;  

def getExtra(key, extraMetaData, defValue):
    if extraMetaData == None:
        return defValue

    if key in extraMetaData:
        return extraMetaData[key]
    return defValue




