from flask_restful import Resource
from flask import make_response, jsonify, request
from globals import globalsSingleton

class OpenEOUdfRuntimes(Resource):
    def get(self):
        return make_response(jsonify(globalsSingleton.openeoip_config["udf_runtimes"]))
