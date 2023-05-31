from flask_restful import Resource
from flask import make_response, jsonify, request
import json
from openeooperation import OpenEoOperation
from globals import globalsSingleton

class OpenEOIPProcessDiscovery(Resource):
    def get(self):
        operations = []
        for operation in globalsSingleton.operations.values() :
            operations.append(operation.toDict())
        processes = {'processes' : operations}            

        return jsonify(processes)

