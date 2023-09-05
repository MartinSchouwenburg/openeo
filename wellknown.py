from flask_restful import Resource
from flask import make_response, jsonify, request

class WellKnown(Resource):

    def __init__(self):
        Resource.__init__(self) 
              
    def get(self):        
        version_list = list()
        version_list.append({"url": "http://127.0.0.1:5000",
                             "api_version": "1.2.0",
                             "production": False})

        resp = dict()
        resp['versions'] = version_list

        return make_response(jsonify(resp), 200)
