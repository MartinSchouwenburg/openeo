from flask_restful import Resource
from flask import make_response, jsonify, request
from globals import globalsSingleton
from constants.constants import *
from processmanager import linkSection
from userinfo import UserInfo

class OpenEOProcessGraphs(Resource):
    def __init__(self):
        Resource.__init__(self)

    def get(self):
        operations = []
        for operation in globalsSingleton.operations.values() :
            if hasattr(operation, 'kind') and (operation.kind  | PDUSERDEFINED) == 1:
                operations.append(operation.toDict())
        processes = {'processes' : operations}       
        processes["links"]  = linkSection(request.base_url, 'processes')

        return make_response(jsonify(processes))
    
    def put(self, process_graph_id):
        request_json = request.get_json()
        user = UserInfo(request)
        
