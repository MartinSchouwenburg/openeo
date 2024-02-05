from flask import jsonify, make_response
from flask_restful import Resource
from globals import globalsSingleton
from eoreader.bands import *
from openeocollections import loadCollections
from rasterdata import RasterData
from processmanager import makeBaseResponseDict
import logging

class OpenEOIPCollection(Resource):
    def get(self, name):
        try:
            raster = globalsSingleton.id2Raster(name)
            if raster == None:
                #no id table found; we have to a complete scan
                loadCollections()
                raster = globalsSingleton.id2Raster(name)
                # if no result then there is no file for this id
                if raster == None:
                    return { "error" : "internal error, id and filename dont match"}
   
            longDict = raster.toLongDictDefinition()
            return make_response(jsonify(longDict),200)
        except Exception as ex:
            logger = logging.getLogger('openeo')
            logger.log(logging.ERROR, str(ex))  
            return make_response(makeBaseResponseDict(-1, 'error', 400, None, str(ex)),400)
        
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
    