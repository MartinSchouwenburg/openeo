from flask_restful import Resource
from flask import make_response, jsonify, request
from globals import globalsSingleton
from constants.constants import *
from processmanager import linkSection

class OpenEOProcessGraph(Resource):
    def get(self, graph_id):
        oper = {}
        for operation in globalsSingleton.operations.values() :
            if hasattr(operation, 'kind') and operation.name == graph_id and (operation.kind  | PDUSERDEFINED) == 1:
                oper = operation.toDict()

        if hasattr(operation, 'sourceGraph'):
            operation['id'] = operation.title
            operation['process_graph'] = operation.sourceGraph
            operation["links"]  = linkSection(request.base_url, graph_id) 
        return make_response(jsonify(operation))