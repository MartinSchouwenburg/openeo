from flask_restful import Resource
from flask import make_response, jsonify, request

API_VERSION = "1.2.0"
API_SHORT_VERSION = "v%s.%s" % (
    API_VERSION.split('.')[0], API_VERSION.split('.')[1])
# This is the URL prefix that is used by app.py and must be used in the tests
URL_PREFIX = "/api/%s" % API_SHORT_VERSION

class WellKnown(Resource):

    def __init__(self):
        Resource.__init__(self) 
              
    def get(self):        
        url = '%s%s/' % (request.root_url.strip('/'), URL_PREFIX)

        version_list = list()
        version_list.append({"url": url,
                             "api_version": API_VERSION,
                             "production": False})

        resp = dict()
        resp['versions'] = version_list

        return make_response(jsonify(resp), 200)
