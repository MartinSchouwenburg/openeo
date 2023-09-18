import os
import json
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
##from globals import openeoip_config
from globals import globalsSingleton
from eoreader.reader import Reader
from eoreader.bands import *
from pathlib import Path
import pickle
import glob
from userinfo import UserInfo
from rasterdata import RasterData

class OpenEOIPCollections(Resource):
    def get(self):
        ##request_json = request.get_json()
        return jsonify(loadCollections()) 
    

def processMetaFile(filename):
    

    return []

def loadCollections():
    user = UserInfo(request)
    data_locations = []
    data_locations.append(globalsSingleton.openeoip_config['data_locations']['root_data_location'])
    loc = globalsSingleton.openeoip_config['data_locations']['root_user_data_location']
    loc['location'] = os.path.join(loc['location'],user.username)
    data_locations.append(loc)

       
    allJson = {}
    allCollections = []

    for location in data_locations:
        path = location["location"]

        extraPath = os.path.join(path, 'extrametadata.json')
        extraMetadataAll = None
        if os.path.exists(extraPath):
            extraMd = open(extraPath)
            extraMetadataAll = json.load(extraMd)  
        if os.path.isdir(path):    
            files = os.listdir(path)
            
            for filename in files:
                collectionJsonDict = {}
                if filename != 'extrametadata.json':
                    fullPath = os.path.join(path,  filename)
                    if os.path.isdir(fullPath):
                        continue 
                    name = os.path.splitext(filename)[0]
                    raster = globalsSingleton.id2Raster(name)
                    if raster == None:
                        try:
                            raster = RasterData()                    

                            if Path(fullPath).suffix == ".metadata":
                                raster.fromMetadataFile(fullPath)
                            else:    
                                extraMetadata = None
                                if filename in extraMetadataAll:
                                    extraMetadata = extraMetadataAll[filename]
                                raster.fromEoReader(fullPath) 
                                   
                        except Exception as ex:
                           continue

                    collectionJsonDict = raster.toShortDictDefinition()
                       
                    if collectionJsonDict != {}:
                        allCollections.append(collectionJsonDict)

    allJson["collections"] = allCollections
    allJson["links"] = globalsSingleton.openeoip_config['links']

    globalsSingleton.saveIdDatabase() 

    return allJson    
         
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




