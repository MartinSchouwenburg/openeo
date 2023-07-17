from flask_restful import Resource
from flask import make_response, jsonify, request
from globals import globalsSingleton
from processmanager import linkSection

class OpenEOIPProcessDiscovery(Resource):
    def get(self):
        operations = []
        for operation in globalsSingleton.operations.values() :
            if hasattr(operation, 'predefined') and operation.predefined:
                operations.append(operation.toDict())
        processes = {'processes' : operations}  
        processes["links"]  = linkSection(request.base_url, 'processes')

        return make_response(jsonify(processes))

