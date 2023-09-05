import os
import json
from flask import Flask, jsonify
from flask_restful import Api, Resource
from globals import globalsSingleton
from eoreader.reader import Reader
from eoreader.bands import *
from pathlib import Path
from openeocollections import createCollectionJson
from openeocollections import checkCache
from openeocollections import save2Cache
from openeocollections import loadCollections

class OpenEOIPCollection(Resource):
    def get(self, name):

        filepath = globalsSingleton.id2filepath(name)
        if filepath == '':
            #no id table found; we have to a complete scan
            loadCollections()
            filepath = globalsSingleton.id2filepath(name)
            # if no result then there is no file for this id
            if filepath == '':
                return { "error" : "internal error, id and filename dont match"}
            
        headpath = os.path.split(filepath)[0]
        filename = os.path.split(filepath)[1]
        extraPath = os.path.join(headpath, 'metadata.json')
        extraMetadataAll = None
        extraMetadata = None
        if os.path.exists(extraPath):
            extraMd = open(extraPath)
            extraMetadataAll = json.load(extraMd)  
            if filename in extraMetadataAll:
                extraMetadata = extraMetadataAll[filename]

        home = Path.home()
        cacheFolder = os.path.join(home, 'Documents/openeo/cache')                
        collectionJsonDict = checkCache(cacheFolder, 'detailed_'+ filename, filepath)
        if ( collectionJsonDict == {}):
            prod = Reader().open(filepath)
            collectionJsonDict = createCollectionJson(prod, extraMetadata, filepath, name)
       
            collectionJsonDict['cube:dimensions'] = self.getDimensions(prod)
            collectionJsonDict['summaries'] = { "constellation" : prod.stac.constellation,
                                        "instruments" : self.getInstrument(prod.instrument)}
            od = prod.get_orbit_direction()
            clouds  = prod.get_cloud_cover()
            collectionJsonDict['eo:cloud_cover'] = [0, clouds]
            collectionJsonDict['proj:epsg'] = { 'min' : prod.stac.proj.epsg, 'max' : prod.stac.proj.epsg}
            bands = prod.bands._band_map
            gsds = set()
            bandlist = []
            for band in bands.items():
                b = band[1]
                if ( b != None):
                    bandlist.append({ 'name' : b.name, 
                                    'common_name' : b.common_name.value,
                                    'center_wavelength' : b.center_wavelength,
                                    "gsd" : b.gsd})
                    gsds.add(b.gsd)

            collectionJsonDict['eo:gsd'] = list(gsds)
            collectionJsonDict['eo:bands'] = bandlist
            save2Cache(collectionJsonDict, filepath, 'detailed_' + filename, cacheFolder)

        return jsonify(collectionJsonDict)
        
    def getInstrument(self, value):
        str(type(value))
        if type(value) == str:
            return value
        if hasattr(value, 'name') and hasattr(value, 'value'):
            return value.value
        
        return str(value) ## probably wrong but at least gives a result
    
    def getDimensions(self, prod):
       proj = prod.stac.proj
       bbox = proj.bbox
       epsg = proj.epsg
       time = [str(prod.stac.datetime)]
       bands = prod.bands
       x =   { 'type' : 'spatial', 'axis' : 'x', 'extent' : [bbox[0], bbox[2]] , 'reference_system' : epsg}
       y =   { 'type' : 'spatial', 'axis' : 'x', 'extent' : [bbox[1], bbox[3]], 'reference_system' : epsg}
       t =   { 'type' : 'temporal', 'extent' : time}

       bandlist = []
       for band in bands.items():
            b = band[1]
            if ( b != None):
                bandlist.append(b.name)

       return { 'x' : x, 'y' : y, 't' : t, 'bands' : { 'type' : 'bands', 'values' : bandlist}}
    