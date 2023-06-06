from flask_restful import Resource
from flask import make_response, jsonify, request
from globals import globalsSingleton
from constants.constants import *

class OpenEOProcessGraphs(Resource):
    def get(self):
        operations = []
        for operation in globalsSingleton.operations.values() :
            if hasattr(operation, 'kind') and (operation.kind  | PDUSERDEFINED) == 1:
                operations.append(operation.toDict())
        processes = {'processes' : operations}            

        return make_response(jsonify(processes))