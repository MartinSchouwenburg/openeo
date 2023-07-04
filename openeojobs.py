from flask import make_response, jsonify, request, session
from flask_restful import Resource
from workflow.openeoprocess import OpenEOProcess
from processmanager import globalProcessManager
from datetime import datetime
from userinfo import UserInfo



class OpenEOIPJobs(Resource):
    def post(self):
        request_doc = request.get_json()
        user = UserInfo(request)
        try:
            process = OpenEOProcess(user, request_doc)
            globalProcessManager.addProcess(process)

            res = { "job_id" : str(process.job_id),
                        "status" : "submitted",
                        "submitted" : str(datetime.now()),
                        "links" : {
                            "href" :  request.base_url + "/" + str(process.job_id),
                            "rel" : 'self',
                            "type" : "application/json"
                        }
                        }
            return make_response(jsonify(res),200)
        except Exception as ex:
            return make_response(jsonify({"job_id" : 0, "job_info" :str(ex)}),404)


    def get(self):
        try:
            user = UserInfo(request)
            jobs = globalProcessManager.allJobs4User(user, None)
            return make_response(jsonify({'jobs' : jobs}),200)
        except Exception as ex:
            return make_response(jsonify({"job_id" : 0, "job_info" :str(ex)}),404)  
        

class OpenEOIPJobs4Job(Resource):
    def get(self, name):
        try:
            user = UserInfo(request)
            jobs = globalProcessManager.allJobs4User(user, name)
            return make_response(jsonify({'jobs' : jobs}),200)
        except Exception as ex:
            return make_response(jsonify({"job_id" : 0, "job_info" :str(ex)}),404)          
        
     

        

        
