from flask import jsonify, request, make_response
from flask_restful import Resource
from processmanager import globalProcessManager, makeBaseResponseDict
from userinfo import UserInfo

class OpenEOIPLogs(Resource):
    def get(self, job_id):
        try:
            user = UserInfo(request)
            logs = globalProcessManager.alllogs4job(user, job_id)
            res = makeBaseResponseDict(job_id, None, 200, request.base_url)
            res['logs'] = logs
            return make_response(jsonify(res),200)
        except Exception as ex:
            return make_response(makeBaseResponseDict(job_id, 'error', 404, None, str(ex)))

        