import sys
import os

pp = os.getcwd()
sys.path.append(pp + '/workflow')
sys.path.append(pp + '/constants')
sys.path.append(pp + '/operations')
sys.path.append(pp)

from flask import Flask, jsonify, make_response
from flask_restful import Api
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix
from globals import globalsSingleton
from openeocollections import OpenEOIPCollections
from openeocapabilities import OpenEOIPCapabilities, OpenEOIPServices, OpenEOIPServiceTypes,replace_links_in_capabilities
from openeocollection import OpenEOIPCollection
from openeoprocessdiscovery import OpenEOIPProcessDiscovery
from openeoresult import OpenEOIPResult
from openeofileformats import OpenEOIPFileFormats
from openeojobs import OpenEOIPJobs, OpenEOMetadata4JobById,OpenEOAddJob2Queue, OpenEOIJobByIdEstimate
from openeoprocessgraphs import OpenEOProcessGraphs
from openeoproccessgraph import OpenEOProcessGraph
from openeologs import OpenEOIPLogs
from openeovalidate import OpenEOIPValidate

from processmanager import globalProcessManager
from threading import Thread

#init part

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1, x_proto=1)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
CORS(app)
api = Api(app)

globalsSingleton.initGlobals()

@app.route('/')
def index():
    CAPABILITIES = replace_links_in_capabilities()
    return make_response(jsonify(CAPABILITIES), 200)


api.add_resource( OpenEOIPCollections,'/collections')
api.add_resource( OpenEOIPCollection,'/collections/<string:name>')
api.add_resource( OpenEOIPCapabilities,'/')
api.add_resource( OpenEOIPProcessDiscovery,'/processes')
api.add_resource( OpenEOIPResult, '/result')
api.add_resource( OpenEOIPFileFormats, '/file_formats')
api.add_resource( OpenEOIPServices, '/services')
api.add_resource( OpenEOIPServiceTypes, '/service_types')
api.add_resource( OpenEOIPJobs, '/jobs') 
api.add_resource( OpenEOMetadata4JobById, '/jobs/<string:job_id>') 
api.add_resource( OpenEOAddJob2Queue, '/jobs/<string:job_id>/results') 
api.add_resource( OpenEOIJobByIdEstimate, '/jobs/<string:job_id>/estimate') 
api.add_resource( OpenEOProcessGraphs, '/process_graphs')
api.add_resource( OpenEOProcessGraph,'/process_graphs/<string:name>')
api.add_resource( OpenEOIPLogs,'/jobs/<string:job_id>/logs')
api.add_resource( OpenEOIPValidate,'/validation')

##api.add_resource( OpenEODelete,'/jobs/<string:job_id>')


def startProcesses():
    globalProcessManager.startProcesses()

t1 = Thread(target=startProcesses)
t1.start()


if __name__ == '__main__':
    app.run()
    globalProcessManager.stop()