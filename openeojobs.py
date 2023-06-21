from flask import make_response, jsonify, request, session
from flask_restful import Resource
from workflow.openeoprocess import OpenEOProcess
from processmanager import globalProcessManager
from datetime import datetime
from userinfo import UserInfo



def runProcess(job):
    if job.workflow != None:
        outputInfo = job.workflow.run(False)


class OpenEOIPJobs(Resource):
    def post(self):
        request_doc = request.get_json()
        user = UserInfo(request)
        try:
            process = OpenEOProcess(request_doc)
            globalProcessManager.addProcess(user.username, process)

            res = { "job_id" : str(process.workflow.job_id),
                        "status" : "submitted",
                        "submitted" : str(datetime.now()),
                        "links" : {
                            "href" :  request.base_url + "/" + str(process.workflow.job_id),
                            "rel" : 'self',
                            "type" : "application/json"
                        }
                        }
            return make_response(jsonify(res),200)
        except Exception as ex:
            return make_response(jsonify({"job_id" : 0, "job_info" :str(ex)}),404)
        
    def get(self):
        return "laters"
        

        
