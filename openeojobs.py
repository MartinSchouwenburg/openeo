from flask import make_response, jsonify, request
from flask_restful import Resource
from workflow.openeoprocess import OpenEOProcess
from processmanager import globalProcessManager
from datetime import datetime
from userinfo import UserInfo
import socket
import json


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
        
            
        
class OpenEOIJobById2(Resource):
   def post(self, job_id):
        request_doc = request.get_json()
        if not 'id' in request_doc:
            return make_response(jsonify({"job_id" : 0, "job_info" :str("missing \'job_id\' key in definition")}),404)  
        
        user = UserInfo(request)
        message = globalProcessManager.queueJob(user, job_id)
        return make_response(jsonify({"job_id" : 0, "job_info" :message}),404)   
    
class OpenEOIJobByIdEstimate(Resource):
   def get(self, job_id):
        user = UserInfo(request)
        estimate = globalProcessManager.makeEstimate(user, job_id)
        costs = estimate[0][2]
        return make_response(jsonify(costs),estimate[1])  
        
class OpenEOIJobById(Resource):
    def get(self, job_id):
        try:
            user = UserInfo(request)
            jobs = globalProcessManager.allJobs4User(user, job_id)
            return make_response(jsonify({'jobs' : jobs}),200)
        except Exception as ex:
            return make_response(jsonify({"job_id" : 0, "job_info" :str(ex)}),404)          

    def delete(self, job_id):
         user = UserInfo(request)
         globalProcessManager.stopJob(user, job_id)
         return make_response(jsonify({"job_id" : job_id, "job_info" :str('has been successfully deleted')}),204) 
     

        

        
