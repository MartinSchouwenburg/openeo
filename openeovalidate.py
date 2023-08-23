from flask_restful import Resource
from flask import make_response, jsonify, request, Response
from constants.constants import *
from workflow.openeoprocess import OpenEOProcess
from userinfo import UserInfo

class OpenEOIPValidate(Resource):
    def post(self):
        request_json = request.get_json()
        user = UserInfo(request)
        process = OpenEOProcess(user, request_json,0)
        errors = process.validate()
        return make_response(jsonify({ "errors": errors}))

 