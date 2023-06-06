from flask import Flask, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
from globals import globalsSingleton
from openeocollections import OpenEOIPCollections
from openeocapabilities import OpenEOIPCapabilities, OpenEOIPServices, OpenEOIPServiceTypes
from openeocollection import OpenEOIPCollection
from openeoprocessdiscovery import OpenEOIPProcessDiscovery
from openeoresult import OpenEOIPResult
from openeofileformats import OpenEOIPFileFormats
from openeojobs import OpenEOIPJobs
from openeoprocessgraphs import OpenEOProcessGraphs
from openeoproccessgraph import OpenEOProcessGraph
from processmanager import globalProcessManager
from threading import Thread

import os
import json
import sqlite3 as sqll3db

#init part
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
CORS(app)
api = Api(app)

globalsSingleton.initGlobals()

api.add_resource( OpenEOIPCollections,'/collections')
api.add_resource( OpenEOIPCollection,'/collection/<string:name>')
api.add_resource( OpenEOIPCapabilities,'/capabilities')
api.add_resource( OpenEOIPProcessDiscovery,'/processes')
api.add_resource( OpenEOIPResult, '/result')
api.add_resource( OpenEOIPFileFormats, '/file_formats')
api.add_resource( OpenEOIPServices, '/services')
api.add_resource( OpenEOIPServiceTypes, '/service_types')
api.add_resource( OpenEOIPJobs, '/jobs') 
api.add_resource( OpenEOProcessGraphs, '/process_graphs')
api.add_resource( OpenEOProcessGraph,'/process_graphs/<string:name>')


def startProcesses():
    globalProcessManager.startProcesses()

t1 = Thread(target=startProcesses)
t1.start()


if __name__ == '__main__':
    app.run()
    globalProcessManager.stop()