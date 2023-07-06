from flask import jsonify, request, make_response
from flask_restful import Resource
from processmanager import globalProcessManager
from userinfo import UserInfo

class OpenEOIPLogs(Resource):
    def get(self, job_id):
        try:
            user = UserInfo(request)
            logs = globalProcessManager.outputs[job_id].logs
            return make_response(jsonify(logs),200)
        except Exception as ex:
            return make_response(jsonify({"job_id" : job_id, "job_info" :str(ex)}),404)  

        