from flask_restful import Resource
from flask import make_response, jsonify, request
from globals import globalsSingleton
from processmanager import linkSection
from constants import constants

class OpenEOIPProcessDiscovery(Resource):
    def __init__(self):
        Resource.__init__(self)

    def get(self):
        operations = []
        for operation in globalsSingleton.operations.values() :
            if hasattr(operation, 'kind') and operation.kind == constants.PDPREDEFINED:
                operations.append(operation.toDict())
        processes = {'processes' : operations}  
        processes["links"]  = linkSection(request.base_url, 'processes')

        return make_response(jsonify(processes))

