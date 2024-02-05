import sys
import os
import pathlib
import logging
import common

def initLogger():
    logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    logger = logging.getLogger('openeo')
    logger.setLevel(logging.INFO)
    logpath = os.path.join(os.path.dirname(__file__), 'log')
    if not os.path.exists(logpath):
        os.mkdir(logpath)
    fileHandler = logging.FileHandler("{0}/{1}.log".format(logpath, ' logfile' ))
    fileHandler.setFormatter(logFormatter)
    logger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    logger.addHandler(consoleHandler)   

initLogger()
common.logMessage(logging.INFO, '----------------------------------------------')
common.logMessage(logging.INFO, 'server started, process id:' + str(os.getpid()))

pp = pathlib.Path(__file__).parent.resolve()
pp = str(pp)
sys.path.append(pp + '/workflow')
sys.path.append(pp + '/constants')
sys.path.append(pp + '/operations')
sys.path.append(pp + '/operations/ilwispy')
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
from openeojobs import OpenEOIPJobs, OpenEOMetadata4JobById,OpenEOJobResults, OpenEOIJobByIdEstimate
from openeoprocessgraphs import OpenEOProcessGraphs
from openeoproccessgraph import OpenEOProcessGraph
from openeologs import OpenEOIPLogs
from openeovalidate import OpenEOIPValidate
from openeoudfruntimes import OpenEOUdfRuntimes
from openeofiles import OpenEODownloadFile

from processmanager import globalProcessManager
from threading import Thread
from wellknown import WellKnown
import common
#from flask import request

#init part

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1, x_proto=1)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

api = Api(app)

globalsSingleton.initGlobals()

common.logMessage(logging.INFO, 'server started, initialization finished')

@app.route('/')
def index():
    CAPABILITIES = replace_links_in_capabilities()
    return make_response(jsonify(CAPABILITIES), 200)

@app.route('/.well-known/openeo')
def well_known():
        return WellKnown.get(api)

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
api.add_resource( OpenEOJobResults, '/jobs/<string:job_id>/results') 
api.add_resource( OpenEOIJobByIdEstimate, '/jobs/<string:job_id>/estimate') 
api.add_resource( OpenEOProcessGraphs, '/process_graphs')
api.add_resource( OpenEOProcessGraph,'/process_graphs/<string:name>')
api.add_resource( OpenEOIPLogs,'/jobs/<string:job_id>/logs')
api.add_resource( OpenEOIPValidate,'/validation')
api.add_resource( OpenEOUdfRuntimes,'/udf_runtimes')
api.add_resource( OpenEODownloadFile,'/files/<string:filepath>')

##api.add_resource( OpenEODelete,'/jobs/<string:job_id>')
CORS(app)

def startProcesses():
    globalProcessManager.startProcesses()

t1 = Thread(target=startProcesses)
t1.start()




if __name__ == '__main__':
    app.run()
    globalProcessManager.stop()