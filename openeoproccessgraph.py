from flask_restful import Resource
from flask import make_response, jsonify, request
from globals import globalsSingleton
from constants.constants import *

class OpenEOProcessGraph(Resource):
    def get(self, name):
        operations = []
        for operation in globalsSingleton.operations.values() :
            if hasattr(operation, 'kind') and operation.name == name and (operation.kind  | PDUSERDEFINED) == 1:
                operations.append(operation.toDict())
        processes = {'processes' : operations}            

        return make_response(jsonify(processes))