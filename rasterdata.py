import os
import json
from eoreader.reader import Reader
from eoreader.bands import *
from globals import globalsSingleton

def isPrimitive(obj):
    return not hasattr(obj, '__dict__')

class RasterLayer:
    def fromMetadata(self, temporalMetadata, idx ):
        self.temporalExtent = temporalMetadata['extent']
        self.dataSource = temporalMetadata['source']
        self.index = idx

class RasterData:
    def fromEoReader(self, filepath):
        extraMetadata = self.loadExtraMetadata(filepath)
        mttime = os.path.getmtime(filepath)
        self.lastmodified = str(mttime)
        prod = Reader().open(filepath)
        self.stac_version = globalsSingleton.openeoip_config['stac_version']
        self.type = 'File'
        namepath = os.path.splitext(filepath)[0]
        head, tail = os.path.split(namepath)
        self.id = tail
        self.title = prod.stac.title
        self.description =  self.getMandatoryValue('description', extraMetadata), 
        self.boundingbox = prod.stac.bbox
        self.license = self.getMandatoryValue('license', extraMetadata),                   
        self.keywords = self.getValue('keywords', extraMetadata, [])
        self.providers = self.getValue('providers', extraMetadata, 'unknown'),
        self.links = self.getMandatoryValue('links', extraMetadata)
        time = [str(prod.stac.datetime), str(prod.stac.datetime)]
        self.temporalExtent = time
        self.dataSource = filepath
        self.dataFolder = ""
        self.epsg = prod.stac.proj.epsg
        self.spatialExtent = prod.stac.proj.bbox
        self.summaries= {}
        self.setSummariesValue('constellation', prod.stac)
        self.setSummariesValue('instrument', prod)
        self.clouds  = prod.get_cloud_cover()
        
        bands = prod.bands._band_map
        self.bands = []
        defnames = ['name', 'common_name', 'description', 'center_wavelength', 'full_width_half_max', 'solar_illumination','gsd']
        for band in bands.items():
            b = band[1]
            if ( b != None):
                att = {"type" : "float"}
                details = {}
                name = ''
                for key,value in b.__dict__.items():
                    if key == 'name':
                        name = value
                    else:
                        if value != None and isPrimitive(value):
                            if key in defnames:
                                details[key] = value
                if name != '':                            
                    att['name'] = name
                att["details"] = details
                self.bands.append(att)
        self.layers = []
        layer = RasterLayer()
        layer.temporalExtent = self.temporalExtent   
        layer.dataSource = self.dataSource
        self.layers.append(layer)

        globalsSingleton.insertRasterInDatabase(self)

    def loadExtraMetadata(self, datapath)  :
        headpath = os.path.split(datapath)[0]
        filename = os.path.split(datapath)[1]
        extraPath = os.path.join(headpath, 'extrametadata.json')
        extraMetadataAll = None
        extraMetadata = None
        if os.path.exists(extraPath):
            extraMd = open(extraPath)
            extraMetadataAll = json.load(extraMd)  
            if filename in extraMetadataAll:
                extraMetadata = extraMetadataAll[filename]
        return extraMetadata
                    
    def fromMetadataFile(self, filepath):
        metafile = open(filepath)
        metadata = json.load(metafile)
        mttime = os.path.getmtime(filepath)
        self.lastmodified = str(mttime)
        self.stac_version = self.getMandatoryValue("stac_version", metadata) 
        self.type = 'Collection' 
        self.id = self.getMandatoryValue("id", metadata) 
        self.title = metadata["title"]
        self.description = self.getMandatoryValue("description", metadata) 
        self.license = self.getMandatoryValue("license", metadata)                   
        self.keywords = self.getValue('keywords', metadata, [])
        self.providers = self.getValue('providers', metadata, 'unknown')
        self.links = self.getMandatoryValue("links", metadata) 
        ext = self.getMandatoryValue("dimensions", metadata)
        self.boundingbox = self.getMandatoryValue("bounding_box", ext)
        self.epsg = self.getValue('epsg' , metadata['projection'], '0')
        temporal = self.getMandatoryValue("t", ext)
        if len(temporal) == 0:
            raise Exception("missing mandatory temporal extent value") 
        first = temporal[0] ## by definition the overall temporal extent
        self.temporalExtent = self.getMandatoryValue("extent", first)
        xext = ext['x']['extent']
        yext = ext['y']['extent']
        self.spatialExtent = [xext[0], xext[1], yext[0], yext[1]]
        namepath = os.path.splitext(filepath)[0]
        head, tail = os.path.split(namepath)
        dataDir = os.path.join(head, metadata["data_folder"])  
        self.dataSource = filepath
        self.dataFolder = dataDir
        self.bands = self.getMandatoryValue("bands", metadata)
        self.layers = []
        for b in range(1, len(temporal)):
            lyr = RasterLayer()
            lyr.fromMetadata(temporal[b], len(self.bands))
            self.layers.append(lyr)
        if 'summaries' in metadata:
            self.summaries = metadata['summaries']            

        globalsSingleton.insertRasterInDatabase(self)

    def toShortDictDefinition(self):
        toplvl_dict = {}

        if hasattr(self, 'id') and self.id != None:
            bbox = {}
            bbox['bbox'] = self.boundingbox
            time = self.temporalExtent
            interval = {}
            interval['interval'] = [time]
            ext = {'spatial' : bbox, 'temporal' : interval}        

            toplvl_dict = {'stac_version' : self.stac_version, 
                    'type' : 'Collection', 
                    'id' : self.id, 
                    'title' : self.title,
                    'description' : self.description, 
                    'extent' : ext,
                    'license' : self.license,                 
                    'keywords' : self.keywords,
                    'providers' : self.providers,
                    'links' : self.links
                    }
        return toplvl_dict
             
    def toLongDictDefinition(self):
        dictDef = self.toShortDictDefinition()
        dictDef['cube:dimensions'] = self.getJsonExtent()
        dictDef['summaries'] = {"constellation" : self.summaries["constellation"], "instrument" : self.summaries['instrument']}
        if hasattr(self, 'clouds'):
            dictDef['eo:cloud_cover'] = [0, self.clouds]
        if hasattr(self, 'snow'):
            dictDef['eo:snow'] = [0, self.snow]            
        dictDef['proj:epsg'] = { 'min' :self.epsg, 'max' : self.epsg} 

        gsds = set()
        bandlist = []
        for b in self.bands:
                if ( b != None):
                    bdef = {"name": b['name']}
                    for kvp in b['details'].items():
                       bdef[kvp[0]] = kvp[1]
                       if kvp[0] == 'gsd':
                            gsds.add(kvp[1])                        
                    bandlist.append(bdef)
        dictDef['eo:bands'] = bandlist
        dictDef['eo:gsd'] = list(gsds)

        return dictDef

    def getValue(self, key, extraMetaData, defValue):
        if extraMetaData == None:
            return defValue

        if key in extraMetaData:
            return extraMetaData[key]
        return defValue

    def setSummariesValue(self, key, source):
        if hasattr(source,key):
            p = getattr(source, key)
            if type(p) == str:
                self.summaries[key] = p
            else:
                if hasattr(source, 'name') and hasattr(source, 'value'):
                    self.summaries[key] = getattr(source,'value')
                else:
                    self.summaries[key] = str(source)
   



    def getMandatoryValue(self, key, extraMetaData):
        if extraMetaData == None:
            raise Exception("missing mandatory key in metadata :" + key)

        if key in extraMetaData:
            return extraMetaData[key]
        raise Exception("missing mandatory key in metadata :" + key)    

    def getJsonExtent(self):
        bbox = self.spatialExtent
        epsg = self.epsg
        time = self.temporalExtent
        bands = self.bands
        x =   { 'type' : 'spatial', 'axis' : 'x', 'extent' : [bbox[0], bbox[2]] , 'reference_system' : epsg}
        y =   { 'type' : 'spatial', 'axis' : 'x', 'extent' : [bbox[1], bbox[3]], 'reference_system' : epsg}
        t =   { 'type' : 'temporal', 'extent' : time}

        eobandlist = []
        for b in bands:
                eobandlist.append(b['name'])

        return { 'x' : x, 'y' : y, 't' : t, 'bands' : { 'type' : 'bands', 'values' : eobandlist}}        

    def getExtentEOReader(self, prod):
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