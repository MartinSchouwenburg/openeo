from flask_restful import Resource
from flask import make_response, jsonify, request
from globals import globalsSingleton
from constants.constants import *

class OpenEOProcessGraph(Resource):
    def get(self, name):
        oper = {}
        for operation in globalsSingleton.operations.values() :
            if hasattr(operation, 'kind') and operation.name == name and (operation.kind  | PDUSERDEFINED) == 1:
                oper = operation.toDict()

        if hasattr(operation, 'sourceGraph'):
            operation['process_graph'] = operation.sourceGraph

        return make_response(jsonify(operation))