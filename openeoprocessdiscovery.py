from flask_restful import Resource
from flask import make_response, jsonify, request
from globals import globalsSingleton

class OpenEOIPProcessDiscovery(Resource):
    def get(self):
        operations = []
        for operation in globalsSingleton.operations.values() :
            if hasattr(operation, 'predefined') and operation.predefined:
                operations.append(operation.toDict())
        processes = {'processes' : operations}            

        return make_response(jsonify(processes))

